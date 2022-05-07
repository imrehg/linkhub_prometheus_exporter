import pytest
from prometheus_client import REGISTRY

from linkhub_prometheus_exporter.exporter import RouterMetrics

# Test payload data
NETWORK_INFO = {
    "PLMN": "12345",
    "NetworkType": 8,
    "NetworkName": "ACMEMobile",
    "SpnName": "",
    "LAC": "0",
    "CellId": "12345",
    "RncId": "reserved",
    "Roaming": 1,
    "Domestic_Roaming": 1,
    "SignalStrength": 4,
    "mcc": "466",
    "mnc": "92",
    "SINR": "17",
    "RSRP": "-90",
    "RSSI": "-62",
    "eNBID": "53561",
    "CGI": "466924d13917",
    "CenterFreq": "0.000000",
    "TxPWR": "0",
    "LTE_state": 239206400,
    "PLMN_name": "N/A",
    "Band": 3,
    "DL_channel": "reserved",
    "UL_channel": "reserved",
    "RSRQ": "-8",
    "EcIo": 0.0,
    "RSCP": -1,
}
SYSTEM_STATUS = {
    "NetworkType": 8,
    "NetworkName": "ACMEMobile",
    "Roaming": 1,
    "Domestic_Roaming": 1,
    "SignalStrength": 4,
    "ConnectionStatus": 2,
    "Conprofileerror": 0,
    "SmsState": 3,
    "VoicemailCount": -16777216,
    "curr_num_2g": 3,
    "curr_num_5g": 0,
    "WlanState": 1,
    "UsbStatus": 1,
    "TotalConnNum": 3,
    "CurrentConnection": 0,
}
USAGE_RECORD = {
    "TConnTimes": 5485256,
    "CurrConnTimes": 88741,
    "HCurrUseUL": 3443105027,
    "HCurrUseDL": 14996934026,
    "HUseData": 18440039053,
    "RCurrUseUL": 0,
    "RCurrUseDL": 0,
    "RoamUseData": 0,
    "MonthlyPlan": 0,
}


def test_metrics(requests_mock):
    """Gathered metrics should be correct based on the response payload."""
    box_addr = "127.0.0.1"
    box_api_url = f"http://{box_addr}/jrd/webapi"

    def matcher(pattern):
        return lambda request: request.json()["method"] == pattern

    requests_mock.post(
        box_api_url,
        json={"result": NETWORK_INFO},
        additional_matcher=matcher("GetNetworkInfo"),
    )
    requests_mock.post(
        box_api_url,
        json={"result": SYSTEM_STATUS},
        additional_matcher=matcher("GetSystemStatus"),
    )
    requests_mock.post(
        box_api_url,
        json={"result": USAGE_RECORD},
        additional_matcher=matcher("GetUsageRecord"),
    )

    # Do a metrics update
    router_metrics = RouterMetrics("", box_addr, 10)
    router_metrics.fetch_new()

    # Compare with expectations
    assert REGISTRY.get_sample_value("sinr") == pytest.approx(
        float(NETWORK_INFO["SINR"])
    )
    assert REGISTRY.get_sample_value("rssi") == pytest.approx(
        float(NETWORK_INFO["RSSI"])
    )
    assert REGISTRY.get_sample_value("rsrp") == pytest.approx(
        float(NETWORK_INFO["RSRP"])
    )
    assert REGISTRY.get_sample_value("rsrq") == pytest.approx(
        float(NETWORK_INFO["RSRQ"])
    )
    assert REGISTRY.get_sample_value("signal_strength") == pytest.approx(
        float(NETWORK_INFO["SignalStrength"])
    )
    assert REGISTRY.get_sample_value("connected_devices") == pytest.approx(
        float(SYSTEM_STATUS["TotalConnNum"])
    )
    assert REGISTRY.get_sample_value("connection_time") == pytest.approx(
        float(USAGE_RECORD["CurrConnTimes"])
    )
    assert REGISTRY.get_sample_value(
        "total_upload_this_month"
    ) == pytest.approx(float(USAGE_RECORD["HCurrUseUL"]))
    assert REGISTRY.get_sample_value(
        "total_download_this_month"
    ) == pytest.approx(float(USAGE_RECORD["HCurrUseDL"]))
    assert REGISTRY.get_sample_value(
        "total_transfer_this_month"
    ) == pytest.approx(float(USAGE_RECORD["HUseData"]))
    # TODO: There should be an easier way to get this
    for item in REGISTRY.collect():
        if item.name == "network_info":
            network_info = item
            break
    assert (
        network_info.samples[0].labels["network_name"]
        == NETWORK_INFO["NetworkName"]
    )
    assert network_info.samples[0].labels["cell_id"] == NETWORK_INFO["CellId"]


@pytest.mark.skip("Not written")
def test_missing_metrics():
    """Test what happens if the scraper couldn't get any metrics."""
    pass
