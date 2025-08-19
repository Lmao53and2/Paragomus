import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    console.log('API Request:', config.method?.toUpperCase(), config.url);
    return config;
  },
  (error) => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    console.log('API Response:', response.status, response.config.url);
    return response;
  },
  (error) => {
    console.error('API Response Error:', error.response?.status, error.message);
    return Promise.reject(error);
  }
);

// API service functions
export const apiService = {
  // Chat endpoints
  async sendMessage(message, context = '') {
    try {
      const response = await api.post('/chat', {
        message,
        context
      });
      return response.data;
    } catch (error) {
      throw new Error(`Failed to send message: ${error.message}`);
    }
  },

  // Task endpoints
  async extractTasks(text) {
    try {
      const response = await api.post('/extract-tasks', {
        text
      });
      return response.data;
    } catch (error) {
      throw new Error(`Failed to extract tasks: ${error.message}`);
    }
  },

  // Personality endpoints
  async getPersonalityProfile() {
    try {
      const response = await api.get('/personality-profile');
      return response.data;
    } catch (error) {
      throw new Error(`Failed to get personality profile: ${error.message}`);
    }
  },

  // UI configuration endpoints
  async getUIConfig(context = '') {
    try {
      const response = await api.post('/ui-config', {
        context
      });
      return response.data;
    } catch (error) {
      throw new Error(`Failed to get UI config: ${error.message}`);
    }
  },

  // Adaptation endpoints
  async getAdaptations() {
    try {
      const response = await api.get('/adaptations');
      return response.data;
    } catch (error) {
      throw new Error(`Failed to get adaptations: ${error.message}`);
    }
  },

  // Full context endpoint
  async getFullContext() {
    try {
      const response = await api.get('/full-context');
      return response.data;
    } catch (error) {
      throw new Error(`Failed to get full context: ${error.message}`);
    }
  },

  // Health check
  async healthCheck() {
    try {
      const response = await api.get('/health');
      return response.data;
    } catch (error) {
      throw new Error(`Health check failed: ${error.message}`);
    }
  }
};

// WebSocket service
export class WebSocketService {
  constructor() {
    this.ws = null;
    this.listeners = new Map();
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
    this.reconnectDelay = 1000;
  }

  connect() {
    try {
      const wsUrl = `ws://localhost:8000/ws`;
      this.ws = new WebSocket(wsUrl);

      this.ws.onopen = () => {
        console.log('WebSocket connected');
        this.reconnectAttempts = 0;
        this.emit('connected');
      };

      this.ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          console.log('WebSocket message received:', data.type);
          this.emit(data.type, data);
        } catch (error) {
          console.error('Failed to parse WebSocket message:', error);
        }
      };

      this.ws.onclose = () => {
        console.log('WebSocket disconnected');
        this.emit('disconnected');
        this.attemptReconnect();
      };

      this.ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        this.emit('error', error);
      };
    } catch (error) {
      console.error('Failed to connect WebSocket:', error);
    }
  }

  disconnect() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }

  send(data) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data));
    } else {
      console.warn('WebSocket not connected, cannot send message');
    }
  }

  sendChatMessage(message, context = '') {
    this.send({
      type: 'chat',
      message,
      context
    });
  }

  requestUIUpdate(context = '') {
    this.send({
      type: 'ui_update',
      context
    });
  }

  on(event, callback) {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, []);
    }
    this.listeners.get(event).push(callback);
  }

  off(event, callback) {
    if (this.listeners.has(event)) {
      const callbacks = this.listeners.get(event);
      const index = callbacks.indexOf(callback);
      if (index > -1) {
        callbacks.splice(index, 1);
      }
    }
  }

  emit(event, data) {
    if (this.listeners.has(event)) {
      this.listeners.get(event).forEach(callback => {
        try {
          callback(data);
        } catch (error) {
          console.error('Error in WebSocket event callback:', error);
        }
      });
    }
  }

  attemptReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      console.log(`Attempting to reconnect WebSocket (${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
      
      setTimeout(() => {
        this.connect();
      }, this.reconnectDelay * this.reconnectAttempts);
    } else {
      console.error('Max reconnection attempts reached');
      this.emit('max_reconnect_attempts_reached');
    }
  }
}

export default apiService;