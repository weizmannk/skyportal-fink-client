# coding: utf-8
from cgi import test
import os
import yaml
from fink_client.consumer import AlertConsumer
from astropy.time import Time
import pandas as pd

import skyportal_fink_client.utils.skyportal_api as skyportal_api
import skyportal_fink_client.utils.files as files
from skyportal_fink_client.utils.switchers import fid_to_filter_ztf
from fink_filters.classification import extract_fink_classification_from_pdf

# open yaml config file
conf = files.yaml_to_dict(
    os.path.abspath(os.path.join(os.path.dirname(__file__))) + "/../config.yaml"
)


def test_poll_alerts():
    """
    Connect to and poll alerts from fink servers to post them in skyportal using its API, using a config file containing
    the necessary access credentials to both fink and skyportal, as well as a list of topics to subscribe to
    (corresponding to a classification in skyportal).

    Parameters
    ----------
    None

    Returns
    ----------
    None
    """
    assert conf["skyportal_token"] is not None
    myconfig = {
        "username": conf["username"],
        "bootstrap.servers": conf["servers"],
        "group_id": conf["group_id"],
    }

    if conf["password"] is not None:
        myconfig["password"] = conf["password"]

    # extract all topics from conf['mytopics'] and create a list of topics names
    topics = list(conf["mytopics"])
    print(f"Fink topics you subscribed to: {topics}")
    print("adding alerts")

    fink_id, stream_id, filter_id = skyportal_api.init_skyportal(
        conf["skyportal_url"], conf["skyportal_token"]
    )

    assert fink_id is not None
    assert stream_id is not None
    assert filter_id is not None
    failed_attempts = 0
    maxtimeout = 5
    # Instantiate a consumer, with a given schema if we are testing with fake alerts
    if conf["testing"] == True:
        print("Using fake alerts for testing")
        schema = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "schemas/schema_test.avsc")
        )
        print(f"Schema used: {schema}")
        consumer = AlertConsumer(topics, myconfig, schema_path=schema)
    else:
        print("Using Fink Broker")
        consumer = AlertConsumer(topics, myconfig)
    try:
        while True:
            if failed_attempts > 2:
                print("No more alerts to process")
                break
            # Poll the servers
            topic, alert, key = consumer.poll(maxtimeout)
            # Analyse output - we just print some values for example
            if topic is not None:
                if alert is not None:
                    classification = extract_fink_classification_from_pdf(
                        pd.DataFrame([alert])
                    )[0]
                    print(
                        f"\nReceived alert from topic {topic} with classification {classification}"
                    )
                    object_id = alert["objectId"]
                    mjd = Time(alert["candidate"]["jd"], format="jd").mjd
                    instruments = ["CFH12k", "ZTF"]
                    filter = fid_to_filter_ztf(
                        alert["candidate"]["fid"]
                    )  # fid is filter id
                    mag = alert["candidate"]["magpsf"]  # to be verified
                    magerr = alert["candidate"]["sigmapsf"]  # to be verified
                    limiting_mag = alert["candidate"]["diffmaglim"]  # to be verified
                    magsys = "ab"  # seems like it is the good magsys
                    ra = alert["candidate"]["ra"]
                    dec = alert["candidate"]["dec"]
                    skyportal_api.from_fink_to_skyportal(
                        classification,
                        object_id,
                        mjd,
                        instruments,
                        filter,
                        mag,
                        magerr,
                        limiting_mag,
                        magsys,
                        ra,
                        dec,
                        fink_id,
                        filter_id,
                        stream_id,
                        url=conf["skyportal_url"],
                        token=conf["skyportal_token"],
                    )
                    topic = None
                    alert = None

            else:
                print("No alerts received in the last {} seconds".format(maxtimeout))
                failed_attempts += 1

    except KeyboardInterrupt:
        print("interrupted!")
        # Close the connection to the servers
        consumer.close()
