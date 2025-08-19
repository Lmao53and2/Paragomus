import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { usePersonality } from './hooks/usePersonality';
import { useWebSocket } from './hooks/useWebSocket';
import ChatInterface from './components/ChatInterface';
import TaskPanel from './components/TaskPanel';
import PersonalityPanel from './components/PersonalityPanel';
import Header from './components/Header';
import LoadingScreen from './components/LoadingScreen';
import ErrorBoundary from './components/ErrorBoundary';
import { LayoutTypes, AnimationLevels } from './types';

function App() {
  const [messages, setMessages] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  
  const {
    personalityProfile,
    adaptations,
    uiConfig,
    loading: personalityLoading,
    error: personalityError,
    updatePersonalityProfile,
    updateAdaptations,
    updateUIConfig,
    getLayoutConfig,
    getAnimationConfig,
    getComponentConfig,
    hasPersonalityData
  } = usePersonality();

  const {
    isConnected,
    connectionError,
    lastMessage,
    sendChatMessage,
    addEventListener,
    removeEventListener
  } = useWebSocket();

  // Handle WebSocket messages
  useEffect(() => {
    const handleChatResponse = (data) => {
      // Add assistant message
      setMessages(prev => [...prev, {
        id: Date.now(),
        type: 'assistant',
        content: data.response,
        timestamp: new Date()
      }]);

      // Update personality data
      if (data.personality_profile) {
        updatePersonalityProfile(data.personality_profile);
      }

      // Update tasks
      if (data.tasks) {
        setTasks(prev => {
          const newTasks = data.tasks.tasks || [];
          return [...prev, ...newTasks.map(task => ({
            ...task,
            id: Date.now() + Math.random(),
            timestamp: new Date()
          }))];
        });
      }

      // Update UI config
      if (data.ui_config) {
        updateUIConfig(data.ui_config);
      }

      // Update adaptations
      if (data.adaptations) {
        updateAdaptations(data.adaptations);
      }
    };

    addEventListener('chat_response', handleChatResponse);

    return () => {
      removeEventListener('chat_response', handleChatResponse);
    };
  }, [addEventListener, removeEventListener, updatePersonalityProfile, updateAdaptations, updateUIConfig]);

  // Handle sending messages
  const handleSendMessage = (message) => {
    // Add user message to chat
    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: message,
      timestamp: new Date()
    };
    
    setMessages(prev => [...prev, userMessage]);

    // Send via WebSocket if connected, otherwise use HTTP API
    if (isConnected) {
      sendChatMessage(message);
    } else {
      // Fallback to HTTP API (implement if needed)
      console.warn('WebSocket not connected, message not sent');
    }
  };

  // Initial loading
  useEffect(() => {
    const timer = setTimeout(() => {
      setIsLoading(false);
    }, 2000);

    return () => clearTimeout(timer);
  }, []);

  // Get layout configuration
  const layoutConfig = getLayoutConfig();
  const animationConfig = getAnimationConfig();
  const chatConfig = getComponentConfig('chatInterface');
  const taskConfig = getComponentConfig('taskDisplay');
  const personalityConfig = getComponentConfig('personalityPanel');

  // Determine layout based on personality
  const getLayoutClass = () => {
    switch (layoutConfig.type) {
      case LayoutTypes.MINIMAL:
        return 'grid-cols-1';
      case LayoutTypes.DETAILED:
        return 'grid-cols-1 lg:grid-cols-4';
      default:
        return 'grid-cols-1 lg:grid-cols-3';
    }
  };

  // Animation variants
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        duration: animationConfig.level === AnimationLevels.NONE ? 0 : 0.5,
        staggerChildren: animationConfig.level === AnimationLevels.FULL ? 0.1 : 0
      }
    }
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1,
      transition: {
        duration: animationConfig.level === AnimationLevels.NONE ? 0 : 0.3
      }
    }
  };

  if (isLoading || personalityLoading) {
    return <LoadingScreen />;
  }

  return (
    <ErrorBoundary>
      <div className="min-h-screen bg-background text-text">
        <Header 
          isConnected={isConnected}
          connectionError={connectionError}
          personalityProfile={personalityProfile}
          layoutConfig={layoutConfig}
        />
        
        <motion.main
          className={`container mx-auto px-4 py-6 grid gap-6 ${getLayoutClass()}`}
          variants={containerVariants}
          initial="hidden"
          animate="visible"
        >
          {/* Chat Interface - Always visible */}
          <motion.div
            className={`${layoutConfig.type === LayoutTypes.DETAILED ? 'lg:col-span-2' : 'lg:col-span-2'}`}
            variants={itemVariants}
          >
            <ChatInterface
              messages={messages}
              onSendMessage={handleSendMessage}
              config={chatConfig}
              animationConfig={animationConfig}
              isConnected={isConnected}
            />
          </motion.div>

          {/* Task Panel - Conditional based on layout */}
          {layoutConfig.type !== LayoutTypes.MINIMAL && (
            <motion.div
              className="lg:col-span-1"
              variants={itemVariants}
            >
              <TaskPanel
                tasks={tasks}
                config={taskConfig}
                animationConfig={animationConfig}
                onTaskUpdate={(updatedTask) => {
                  setTasks(prev => prev.map(task => 
                    task.id === updatedTask.id ? updatedTask : task
                  ));
                }}
              />
            </motion.div>
          )}

          {/* Personality Panel - Conditional based on layout and config */}
          {layoutConfig.type === LayoutTypes.DETAILED && personalityConfig.visible && (
            <motion.div
              className="lg:col-span-1"
              variants={itemVariants}
            >
              <PersonalityPanel
                personalityProfile={personalityProfile}
                adaptations={adaptations}
                config={personalityConfig}
                animationConfig={animationConfig}
              />
            </motion.div>
          )}
        </motion.main>

        {/* Floating Personality Panel for other layouts */}
        <AnimatePresence>
          {layoutConfig.type !== LayoutTypes.DETAILED && 
           personalityConfig.visible && 
           personalityConfig.position === 'modal' && 
           hasPersonalityData() && (
            <motion.div
              className="fixed bottom-4 right-4 z-50"
              initial={{ scale: 0, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0, opacity: 0 }}
              transition={{ duration: 0.3 }}
            >
              <PersonalityPanel
                personalityProfile={personalityProfile}
                adaptations={adaptations}
                config={{ ...personalityConfig, compact: true }}
                animationConfig={animationConfig}
              />
            </motion.div>
          )}
        </AnimatePresence>

        {/* Error Display */}
        <AnimatePresence>
          {(personalityError || connectionError) && (
            <motion.div
              className="fixed top-4 right-4 bg-red-500 text-white p-4 rounded-lg shadow-lg z-50"
              initial={{ x: 300, opacity: 0 }}
              animate={{ x: 0, opacity: 1 }}
              exit={{ x: 300, opacity: 0 }}
              transition={{ duration: 0.3 }}
            >
              <p className="font-medium">Error</p>
              <p className="text-sm">
                {personalityError || connectionError?.message || 'Unknown error'}
              </p>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </ErrorBoundary>
  );
}

export default App;