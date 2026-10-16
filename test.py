from unittest.mock import Mock,patch
from github_api import get_repo_info

response=Mock()
for status in[403,404]:
    response.status_code=status
    with patch("github_api.requests.get") as mock_get:
        mock_get.return_value=response
        results=get_repo_info("python/cpython")
        print(results)
        assert results==(None,None)
        mock_get.assert_called_once()