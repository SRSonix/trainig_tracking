from typing import List, Dict, Any, Optional

from loguru import logger

from shared_models.schemas import Skill, Exercise

import requests


class ClientException(Exception):
    ...

class TraningTrackingClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        
    @staticmethod
    def _to_query_params(**kwargs) -> Optional[Dict[str, str]]:
        if len(kwargs) == 0:
            return None

        query_params = {}
        for key, value in kwargs.items():
            if value is not None:
                query_params[key] = value
        
        return query_params 
        

    def _request(self, endpoint, method, body: str=None, query_params: Optional[Dict[str, str]] = None):
        url = f"{self.base_url}/{endpoint}"
        
        if method == "get":
            if body is not None:
                raise ClientException("Get requerst does not support body.")
            response = requests.get(url, params=query_params)
        elif method == "post":
            if query_params is not None:
                raise ClientException("Post requerst does not support query_params.")
            response = requests.post(url, data=body)
        elif method == "delete":
            if body is not None:
                raise ClientException("Delete requerst does not support body.")
            if query_params is not None:
                raise ClientException("Delete requerst does not support query_params.")
            response = requests.delete(url)
        else: 
            raise NotImplementedError(f"Request method {method} is not implemented in this client.")
        
        if response.status_code != 200:
            logger.warning(f"Got status code {response.status_code}.")
            logger.warning(url)
            if response.status_code != 500:
                logger.warning(response.json()["detail"])
            raise ClientException(f"Got status code {response.status_code}.")

        return response

    def _get(self, endpoint: str, query_params: Optional[Dict[str, str]] = None):
        return self._request(endpoint=endpoint, method="get", query_params=query_params)
        
    def _post(self, endpoint: str, body: str):
        return self._request(endpoint=endpoint, method="post", body=body)
    
    def _delete(self, endpoint: str):
        return self._request(endpoint=endpoint, method="delete")
        
    def assert_api_health(self):
        response = self._get("health/")
        
        if response.status_code != 200:
            raise ClientException("API not healthy.")
    
    def get_skills(self, id: Optional[str]=None, domain: Optional[str]=None) -> List[Skill]:
        query_params = self._to_query_params(id=id, domain=domain)
        response = self._get("skills/", query_params=query_params)
        
        return [Skill.parse_obj(s) for s in response.json()]
    
    def post_skill(self, skill: Skill):
        self._post("skills/", body=skill.json())
        
    def delete_skill(self, id:str):
        self._delete(f"skills/{id}")
    
    def get_exercises(self) -> List[Exercise]:
        response = self._get("exercises/")
        
        return [Exercise.parse_obj(s) for s in response.json()]
    
    def post_exercise(self, exercise: Exercise):
        self._post("exercises/", body=exercise.json())
        
    def delete_exercise(self, id:str, variation:str):
        self._delete(f"exercises/{id}/{variation}")
    