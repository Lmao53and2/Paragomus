import { useState, useEffect, useRef, useCallback } from 'react';
import { WebSocketService } from '../services/api';

export const useWebSocket = () => {
  const [isConnected, setIsConnected] = useState(false);
  const [connectionError, setConnectionError] = useState(null);
  const [lastMessage, setLastMessage] = useState(null);
  const wsRef = useRef(null);

  // Initialize WebSocket connection
  useEffect(() => {
    wsRef.current = new WebSocketService();
    
    // Set up event listeners
    wsRef.current.on('connected', () => {
      setIsConnected(true);
      setConnectionError(null);
    });

    wsRef.current.on('disconnected', () => {
      setIsConnected(false);
    });

    wsRef.current.on('error', (error) => {
      setConnectionError(error);
    });

    wsRef.current.on('chat_response', (data) => {
      setLastMessage(data);
    });

    wsRef.current.on('ui_config', (data) => {
      setLastMessage(data);
    });

    wsRef.current.on('max_reconnect_attempts_reached', () => {
      setConnectionError(new Error('Maximum reconnection attempts reached'));
    });

    // Connect
    wsRef.current.connect();

    // Cleanup on unmount
    return () => {
      if (wsRef.current) {
        wsRef.current.disconnect();
      }
    };
  }, []);

  // Send chat message
  const sendChatMessage = useCallback((message, context = '') => {
    if (wsRef.current) {
      wsRef.current.sendChatMessage(message, context);
    }
  }, []);

  // Request UI update
  const requestUIUpdate = useCallback((context = '') => {
    if (wsRef.current) {
      wsRef.current.requestUIUpdate(context);
    }
  }, []);

  // Add event listener
  const addEventListener = useCallback((event, callback) => {
    if (wsRef.current) {
      wsRef.current.on(event, callback);
    }
  }, []);

  // Remove event listener
  const removeEventListener = useCallback((event, callback) => {
    if (wsRef.current) {
      wsRef.current.off(event, callback);
    }
  }, []);

  // Reconnect manually
  const reconnect = useCallback(() => {
    if (wsRef.current) {
      wsRef.current.disconnect();
      setTimeout(() => {
        wsRef.current.connect();
      }, 1000);
    }
  }, []);

  return {
    isConnected,
    connectionError,
    lastMessage,
    sendChatMessage,
    requestUIUpdate,
    addEventListener,
    removeEventListener,
    reconnect
  };
};