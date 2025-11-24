const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

async function apiCall(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  const token = localStorage.getItem('token');
  
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };
  
  if (token && !options.skipAuth) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  
  try {
    // console.log('API Call:', url, options);
    const response = await fetch(url, {
      ...options,
      headers,
    });
    
    // console.log('API Response:', response.status, response.statusText);
    
    if (!response.ok) {
      const error = await response.json();
      console.error('API Error Response:', error);
      throw new Error(error.detail || 'API request failed');
    }
    
    const data = await response.json();
    // console.log('API Success Data:', data);
    return data;
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
}

export const authAPI = {
  register: async (email, username, password) => {
    const data = await apiCall('/auth/register', {
      method: 'POST',
      body: JSON.stringify({ email, username, password }),
      skipAuth: true,
    });
    
    localStorage.setItem('token', data.access_token);
    localStorage.setItem('user', JSON.stringify(data.user));
    localStorage.setItem('userId', data.user.id);
    localStorage.setItem('isAuthenticated', 'true');
    
    return data;
  },
  
  login: async (email, password) => {
    const data = await apiCall('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
      skipAuth: true,
    });
    
    localStorage.setItem('token', data.access_token);
    localStorage.setItem('user', JSON.stringify(data.user));
    localStorage.setItem('userId', data.user.id);
    localStorage.setItem('isAuthenticated', 'true');
    
    return data;
  },
  
  getCurrentUser: async () => {
    return await apiCall('/auth/me');
  },
  
  logout: () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    localStorage.removeItem('userId');
    localStorage.removeItem('isAuthenticated');
  },
  
  isAuthenticated: () => {
    return !!localStorage.getItem('token');
  },
  
  getUser: () => {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
  },
};

export const charactersAPI = {
  getAll: async () => {
    return await apiCall('/characters');
  },
  
  getById: async (characterId) => {
    return await apiCall(`/characters/${characterId}`);
  },
};

export const chatAPI = {
  sendMessage: async (characterId, message, conversationId = null) => {
    const userId = localStorage.getItem('userId');
    
    return await apiCall('/chat', {
      method: 'POST',
      body: JSON.stringify({
        character_id: characterId,
        message: message,
        conversation_id: conversationId,
        user_id: userId,
      }),
    });
  },
  
  getConversation: async (conversationId) => {
    return await apiCall(`/conversations/${conversationId}`);
  },
  
  getConversations: async () => {
    return await apiCall('/conversations');
  },

  clearMemory: async (characterId) => {
    const userId = localStorage.getItem('userId');
    return await apiCall('/chat/clear', {
      method: 'POST',
      body: JSON.stringify({
        character_id: characterId,
        user_id: userId
      })
    });
  }
};

export const healthAPI = {
  check: async () => {
    return await apiCall('/health');
  },
  
  info: async () => {
    return await apiCall('/info');
  },
};

const API = {
  auth: authAPI,
  characters: charactersAPI,
  chat: chatAPI,
  health: healthAPI,
};

export default API;
