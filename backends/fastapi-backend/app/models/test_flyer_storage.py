import concurrent.futures

from httpx import get

from app.models.flyer_storage import FlyerStorage, get_storage
from io import BytesIO

from app.services.flyer_generator.flyer import Flyer

def insert_into(i: int, storage: FlyerStorage) -> str|None:
    content = BytesIO()
    content.write(i.to_bytes(4, byteorder='big'))
    return storage.store(content)

def read_from(uri: str, storage: FlyerStorage) -> int:
    bcontent = storage.get(uri)
    assert bcontent != None
    # read 4 bytes from buffer and convert to an integer.
    return int.from_bytes(bcontent.getvalue(), byteorder='big', signed=True)


def test_flyer_storage():
    storage = get_storage()
    ids = []
    uri_to_value = {}
    for i in range(10):
        uri = insert_into(i, storage)
        assert uri != None
        uri_to_value[uri] = i
        ids.append(uri)
    assert len(storage) == 10
    assert len(ids) == 10

    for uri in ids:
        value = read_from(uri, storage)
        assert value == uri_to_value[uri]

    assert len(storage) == 0


def test_multithreaded_flyer_storage():
    items = [i for i in range(1000)]
    storage = get_storage()
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_list_of_uris = [executor.submit(insert_into, item, storage) for item in items]
        concurrent.futures.wait(future_list_of_uris)
        assert len(storage) == len(items)
        uris = [future.result() for future in future_list_of_uris]
        uris = [ "" if uri == None else uri for uri in uris ]
        future_list_of_recovered_items = [ executor.submit(read_from, uri, storage) for uri in uris ]
        concurrent.futures.wait(future_list_of_recovered_items)
        recovered_items = [ future.result() for future in future_list_of_recovered_items ]

        assert len(recovered_items) == len(items)
        recovered_items.sort()
        assert recovered_items == items
    assert len(storage) == 0
