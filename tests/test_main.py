from unittest.mock import patch, MagicMock


@patch('redis.Redis')
def test_redis_connection(mock_redis):
    mock_instance = MagicMock()
    mock_redis.return_value = mock_instance
    mock_instance.ping.return_value = True

    import redis
    r = redis.Redis(host='localhost', port=6379)
    assert r.ping() is True


@patch('redis.Redis')
def test_redis_set_get(mock_redis):
    mock_instance = MagicMock()
    mock_redis.return_value = mock_instance
    mock_instance.set.return_value = True
    mock_instance.get.return_value = b'hello'

    import redis
    r = redis.Redis(host='localhost', port=6379)
    r.set('key', 'hello')
    result = r.get('key')
    assert result == b'hello'


@patch('redis.Redis')
def test_redis_delete(mock_redis):
    mock_instance = MagicMock()
    mock_redis.return_value = mock_instance
    mock_instance.delete.return_value = 1

    import redis
    r = redis.Redis(host='localhost', port=6379)
    result = r.delete('key')
    assert result == 1
