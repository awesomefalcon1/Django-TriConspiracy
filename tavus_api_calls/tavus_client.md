"""
Tavus API Client
A comprehensive wrapper for the Tavus Conversational Video Interface API
"""

import requests
import json
from typing import Optional, Dict, Any
from django.conf import settings


class TavusAPIError(Exception):
    """Custom exception for Tavus API errors"""
    pass


class TavusClient:
    """
    Client for interacting with the Tavus API
    """
      def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Tavus client
        
        Args:
            api_key (str, optional): Tavus API key. If not provided, will try to get from settings
        """
        self.api_key = api_key or getattr(settings, 'TAVUS_API_KEY', None)
        if not self.api_key:
            raise ValueError("Tavus API key is required. Set TAVUS_API_KEY in .env file or pass api_key parameter.")
        
        self.base_url = "https://tavusapi.com/v2"
        self.headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json"
        }
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Make a request to the Tavus API
        
        Args:
            method (str): HTTP method (GET, POST, DELETE, etc.)
            endpoint (str): API endpoint
            data (dict, optional): Request payload
            
        Returns:
            dict: API response
            
        Raises:
            TavusAPIError: If the API request fails
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=self.headers)
            elif method.upper() == "POST":
                response = requests.post(url, headers=self.headers, json=data)
            elif method.upper() == "DELETE":
                response = requests.delete(url, headers=self.headers)
            elif method.upper() == "PATCH":
                response = requests.patch(url, headers=self.headers, json=data)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            # Check if request was successful
            response.raise_for_status()
            
            # Return JSON response if available
            try:
                return response.json()
            except json.JSONDecodeError:
                return {"status": "success", "response": response.text}
                
        except requests.exceptions.RequestException as e:
            raise TavusAPIError(f"API request failed: {str(e)}")
    
    # Conversation Methods
    
    def create_conversation(
        self,
        replica_id: Optional[str] = None,
        persona_id: Optional[str] = None,
        callback_url: Optional[str] = None,
        conversation_name: Optional[str] = None,
        conversational_context: Optional[str] = None,
        custom_greeting: Optional[str] = None,
        properties: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a new conversation with a replica
        
        Args:
            replica_id (str, optional): The unique identifier for the replica
            persona_id (str, optional): The unique identifier for the persona
            callback_url (str, optional): URL for webhook updates
            conversation_name (str, optional): Name for the conversation
            conversational_context (str, optional): Additional context for the conversation
            custom_greeting (str, optional): Custom greeting message
            properties (dict, optional): Additional conversation properties
            
        Returns:
            dict: Conversation details including conversation_id and conversation_url
            
        Note:
            Either replica_id or persona_id must be provided
        """
        payload = {}
        
        # At least one of replica_id or persona_id must be provided
        if not replica_id and not persona_id:
            raise ValueError("Either replica_id or persona_id must be provided")
        
        if replica_id:
            payload["replica_id"] = replica_id
        if persona_id:
            payload["persona_id"] = persona_id
        if callback_url:
            payload["callback_url"] = callback_url
        if conversation_name:
            payload["conversation_name"] = conversation_name
        if conversational_context:
            payload["conversational_context"] = conversational_context
        if custom_greeting:
            payload["custom_greeting"] = custom_greeting
        if properties:
            payload["properties"] = properties
        
        return self._make_request("POST", "conversations", payload)
    
    def get_conversation(self, conversation_id: str) -> Dict[str, Any]:
        """
        Get details of a specific conversation
        
        Args:
            conversation_id (str): The unique identifier for the conversation
            
        Returns:
            dict: Conversation details
        """
        return self._make_request("GET", f"conversations/{conversation_id}")
    
    def list_conversations(self) -> Dict[str, Any]:
        """
        List all conversations
        
        Returns:
            dict: List of conversations
        """
        return self._make_request("GET", "conversations")
    
    def end_conversation(self, conversation_id: str) -> Dict[str, Any]:
        """
        End a specific conversation
        
        Args:
            conversation_id (str): The unique identifier for the conversation
            
        Returns:
            dict: Response confirming the conversation was ended
        """
        return self._make_request("POST", f"conversations/{conversation_id}/end")
    
    def delete_conversation(self, conversation_id: str) -> Dict[str, Any]:
        """
        Delete a specific conversation
        
        Args:
            conversation_id (str): The unique identifier for the conversation
            
        Returns:
            dict: Response confirming the conversation was deleted
        """
        return self._make_request("DELETE", f"conversations/{conversation_id}")
    
    # Replica Methods
    
    def create_replica(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new replica
        
        Args:
            data (dict): Replica creation data
            
        Returns:
            dict: Replica details
        """
        return self._make_request("POST", "replicas", data)
    
    def get_replica(self, replica_id: str) -> Dict[str, Any]:
        """
        Get details of a specific replica
        
        Args:
            replica_id (str): The unique identifier for the replica
            
        Returns:
            dict: Replica details
        """
        return self._make_request("GET", f"replicas/{replica_id}")
    
    def list_replicas(self) -> Dict[str, Any]:
        """
        List all replicas
        
        Returns:
            dict: List of replicas
        """
        return self._make_request("GET", "replicas")
    
    def delete_replica(self, replica_id: str) -> Dict[str, Any]:
        """
        Delete a specific replica
        
        Args:
            replica_id (str): The unique identifier for the replica
            
        Returns:
            dict: Response confirming the replica was deleted
        """
        return self._make_request("DELETE", f"replicas/{replica_id}")
    
    def rename_replica(self, replica_id: str, name: str) -> Dict[str, Any]:
        """
        Rename a specific replica
        
        Args:
            replica_id (str): The unique identifier for the replica
            name (str): New name for the replica
            
        Returns:
            dict: Updated replica details
        """
        return self._make_request("PATCH", f"replicas/{replica_id}", {"name": name})
    
    # Persona Methods
    
    def create_persona(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new persona
        
        Args:
            data (dict): Persona creation data
            
        Returns:
            dict: Persona details
        """
        return self._make_request("POST", "personas", data)
    
    def get_persona(self, persona_id: str) -> Dict[str, Any]:
        """
        Get details of a specific persona
        
        Args:
            persona_id (str): The unique identifier for the persona
            
        Returns:
            dict: Persona details
        """
        return self._make_request("GET", f"personas/{persona_id}")
    
    def list_personas(self) -> Dict[str, Any]:
        """
        List all personas
        
        Returns:
            dict: List of personas
        """
        return self._make_request("GET", "personas")
    
    def patch_persona(self, persona_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a specific persona
        
        Args:
            persona_id (str): The unique identifier for the persona
            data (dict): Update data
            
        Returns:
            dict: Updated persona details
        """
        return self._make_request("PATCH", f"personas/{persona_id}", data)
    
    def delete_persona(self, persona_id: str) -> Dict[str, Any]:
        """
        Delete a specific persona
        
        Args:
            persona_id (str): The unique identifier for the persona
            
        Returns:
            dict: Response confirming the persona was deleted
        """
        return self._make_request("DELETE", f"personas/{persona_id}")
