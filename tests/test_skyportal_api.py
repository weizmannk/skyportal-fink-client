import yaml
import os
import skyportal_fink_client.utils.skyportal_api as skyportal_api
import skyportal_fink_client.utils.files as files

conf = files.yaml_to_dict(
    os.path.abspath(os.path.join(os.path.dirname(__file__))) + "/../config.yaml"
)
skyportal_token = conf["skyportal_token"]


def test_get_all_groups_id():
    status, data = skyportal_api.get_all_group_ids(
        "http://localhost:5000", skyportal_token
    )
    assert status == 200
    assert data is not None


def test_get_group_ids_and_name():
    status, data = skyportal_api.get_group_ids_and_name(
        "http://localhost:5000", skyportal_token
    )
    assert status == 200
    assert data is not None


def test_get_all_instruments():
    status, data = skyportal_api.get_all_instruments(
        "http://localhost:5000", skyportal_token
    )
    assert status == 200
    assert data is not None


def test_get_all_source_ids():
    status, data = skyportal_api.get_all_source_ids(
        "http://localhost:5000", skyportal_token
    )
    assert status == 200
    assert data is not None


def test_get_all_candidate_ids():
    status, data = skyportal_api.get_all_candidate_ids(
        "http://localhost:5000", skyportal_token
    )
    assert status == 200
    assert data is not None


def test_get_all_streams():
    status, data = skyportal_api.get_all_streams(
        "http://localhost:5000", skyportal_token
    )
    assert status == 200
    assert data is not None


def test_get_all_stream_ids():
    status, data = skyportal_api.get_all_stream_ids(
        "http://localhost:5000", skyportal_token
    )
    assert status == 200
    assert data is not None


def test_classification_exists_for_objs():
    result = skyportal_api.classification_exists_for_objs(
        "ZTF18aabcvnq", "http://localhost:5000", skyportal_token
    )
    assert result is not None
    assert result == True


def test_classification_id_for_objs():
    status, data = skyportal_api.classification_id_for_objs(
        "ZTF18aabcvnq", "http://localhost:5000", skyportal_token
    )
    assert status == 200
    assert data is not None


def test_post_source():
    status, data = skyportal_api.post_source(
        "ZTFtestAPI",
        5,
        5,
        [1],
        "http://localhost:5000",
        skyportal_token,
    )
    assert status == 200
    assert data is not None


def test_post_candidate():
    status, data = skyportal_api.post_candidate(
        "ZTFtestAPI",
        5,
        5,
        [1],
        "2022-04-11 06:27:01.728",
        "http://localhost:5000",
        skyportal_token,
    )
    assert status == 200
    assert data is not None


def test_post_photometry():
    status, data = skyportal_api.post_photometry(
        "ZTF21aaqjmps",
        59580.0,
        1,
        "ztfr",
        19.0,
        0.1,
        21.0,
        "ab",
        5,
        5,
        [1],
        [1],
        "http://localhost:5000",
        skyportal_token,
    )
    assert status == 200
    assert data is not None


def test_post_classification():
    status, data = skyportal_api.post_classification(
        "ZTF21aaqjmps",
        "kilonova",
        1,
        [1],
        "http://localhost:5000",
        skyportal_token,
    )
    assert status == 200
    assert data is not None


def test_post_streams():
    status, data = skyportal_api.post_streams(
        "StreamTestAPI",
        "http://localhost:5000",
        skyportal_token,
    )
    assert status == 200
    assert data is not None


def test_post_filters():
    status, data = skyportal_api.post_filters(
        "FilterTestAPI",
        1,
        1,
        "http://localhost:5000",
        skyportal_token,
    )
    assert status == 200
    assert data is not None


def test_post_telescopes():
    status, data = skyportal_api.post_telescopes(
        "TelescopeTestAPI",
        "TTAPI",
        20.0,
        "http://localhost:5000",
        skyportal_token,
    )
    assert status == 200
    assert data is not None


def test_post_instruments():
    status, data = skyportal_api.post_instruments(
        "InstrumentTestAPI",
        "imager",
        1,
        ["ztfr", "ztfg", "ztfi"],
        "http://localhost:5000",
        skyportal_token,
    )
    assert status == 200
    assert data is not None


def test_post_groups():
    status, data = skyportal_api.post_groups(
        "GroupTestAPI",
        "http://localhost:5000",
        skyportal_token,
    )
    assert status == 200
    assert data is not None


def test_post_taxonomy():
    hierarchy = {"class": "classificationTestAPI"}
    status, data = skyportal_api.post_taxonomy(
        "TaxonomyTestAPI",
        hierarchy,
        "1",
        "http://localhost:5000",
        skyportal_token,
    )
    assert status == 200
    assert data is not None


def test_update_classification():
    status = skyportal_api.update_classification(
        "ZTF18aabcvnq",
        "kilonova",
        1,
        [1],
        "http://localhost:5000",
        skyportal_token,
    )
    assert status == 200


def test_get_all_filters():
    status, data = skyportal_api.get_all_filters(
        "http://localhost:5000", skyportal_token
    )
    assert status == 200
    assert data is not None


def test_get_all_taxonomies():
    status, data = skyportal_api.get_all_taxonomies(
        "http://localhost:5000", skyportal_token
    )
    assert status == 200
    assert data is not None


def test_class_exists_in_hierarchy():
    classification_name, exists = skyportal_api.class_exists_in_hierarchy(
        "classificationTestAPI".lower(),
        [{"class": "test", "subclasses": [{"class": "classificationTestAPI"}]}],
    )
    assert classification_name is not None
    assert exists == True


def test_get_taxonomy_id_including_classification():
    hierarchy = {"class": "test", "subclasses": [{"class": "classificationTestAPI2"}]}
    status, data = skyportal_api.post_taxonomy(
        "TaxonomyTestAPI2",
        hierarchy,
        "1",
        "http://localhost:5000",
        skyportal_token,
    )
    assert status == 200
    assert data is not None

    (
        status,
        classification,
        taxonomy_id,
    ) = skyportal_api.get_taxonomy_id_including_classification(
        "classificationTestAPI2", "http://localhost:5000", skyportal_token
    )
    assert status == 200
    assert classification is not None
    assert taxonomy_id is not None


def test_init_skyportal():
    result = skyportal_api.init_skyportal("http://localhost:5000", skyportal_token)
    assert result is not None
    assert result[0] is not None
    assert result[1] is not None
    assert result[2] is not None


def test_from_fink_to_skyportal():
    fink_id, stream_id, filter_id = skyportal_api.init_skyportal(
        "http://localhost:5000", skyportal_token
    )
    result = skyportal_api.from_fink_to_skyportal(
        "kilonova",
        "ZTFAPITESTFINAL",
        59000.0,
        "ZTF",
        "ztfr",
        17,
        0.1,
        21,
        "ab",
        5.0,
        5.0,
        fink_id,
        filter_id,
        stream_id,
        "http://localhost:5000",
        skyportal_token,
    )

    assert result is not None
    assert result == 200
