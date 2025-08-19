import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Bot, User, Loader } from 'lucide-react';
import { MessageTypes, AnimationLevels } from '../types';

const ChatInterface = ({ 
  messages, 
  onSendMessage, 
  config, 
  animationConfig, 
  isConnected 
}) => {
  const [inputMessage, setInputMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Handle form submission
  const handleSubmit = (e) => {
    e.preventDefault();
    if (inputMessage.trim() && isConnected) {
      onSendMessage(inputMessage.trim());
      setInputMessage('');
      setIsTyping(true);
      
      // Simulate typing indicator
      setTimeout(() => setIsTyping(false), 2000);
    }
  };

  // Handle key press
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  // Get message style based on config
  const getMessageStyle = () => {
    switch (config.style) {
      case 'linear':
        return 'border-l-4 border-primary pl-4 py-2';
      case 'card':
        return 'bg-white dark:bg-gray-800 rounded-lg shadow-md p-4';
      default: // bubble
        return 'rounded-2xl px-4 py-2';
    }
  };

  // Get spacing class
  const getSpacingClass = () => {
    switch (config.messageSpacing) {
      case 'compact':
        return 'space-y-2';
      case 'spacious':
        return 'space-y-6';
      default:
        return 'space-y-4';
    }
  };

  // Animation variants
  const messageVariants = {
    hidden: { 
      opacity: 0, 
      y: 20,
      scale: animationConfig.level === AnimationLevels.FULL ? 0.9 : 1
    },
    visible: { 
      opacity: 1, 
      y: 0,
      scale: 1,
      transition: {
        duration: animationConfig.level === AnimationLevels.NONE ? 0 : 0.3,
        ease: 'easeOut'
      }
    }
  };

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: animationConfig.level === AnimationLevels.FULL ? 0.1 : 0
      }
    }
  };

  return (
    <div className="flex flex-col h-[600px] bg-white dark:bg-gray-900 rounded-lg shadow-lg overflow-hidden">
      {/* Header */}
      <div className="bg-primary text-white px-6 py-4 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <Bot className="w-6 h-6" />
          <h2 className="text-lg font-semibold">AI Assistant</h2>
        </div>
        <div className="flex items-center space-x-2">
          <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-400' : 'bg-red-400'}`} />
          <span className="text-sm">{isConnected ? 'Connected' : 'Disconnected'}</span>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-6 scrollbar-thin">
        <motion.div
          className={getSpacingClass()}
          variants={containerVariants}
          initial="hidden"
          animate="visible"
        >
          <AnimatePresence>
            {messages.map((message) => (
              <motion.div
                key={message.id}
                className={`flex ${message.type === MessageTypes.USER ? 'justify-end' : 'justify-start'}`}
                variants={messageVariants}
                initial="hidden"
                animate="visible"
                exit="hidden"
                layout={animationConfig.level === AnimationLevels.FULL}
              >
                <div className={`max-w-[80%] ${getMessageStyle()} ${
                  message.type === MessageTypes.USER
                    ? 'bg-primary text-white'
                    : 'bg-gray-100 dark:bg-gray-800 text-text'
                }`}>
                  <div className="flex items-start space-x-3">
                    <div className="flex-shrink-0">
                      {message.type === MessageTypes.USER ? (
                        <User className="w-5 h-5 mt-1" />
                      ) : (
                        <Bot className="w-5 h-5 mt-1" />
                      )}
                    </div>
                    <div className="flex-1">
                      <p className="text-sm leading-relaxed whitespace-pre-wrap">
                        {message.content}
                      </p>
                      {config.showTimestamps && (
                        <p className="text-xs opacity-70 mt-2">
                          {message.timestamp.toLocaleTimeString()}
                        </p>
                      )}
                    </div>
                  </div>
                </div>
              </motion.div>
            ))}
          </AnimatePresence>

          {/* Typing indicator */}
          <AnimatePresence>
            {isTyping && (
              <motion.div
                className="flex justify-start"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
              >
                <div className={`${getMessageStyle()} bg-gray-100 dark:bg-gray-800`}>
                  <div className="flex items-center space-x-3">
                    <Bot className="w-5 h-5" />
                    <div className="flex space-x-1">
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" />
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }} />
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }} />
                    </div>
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </motion.div>
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="border-t border-gray-200 dark:border-gray-700 p-4">
        <form onSubmit={handleSubmit} className="flex space-x-3">
          <div className="flex-1 relative">
            <textarea
              ref={inputRef}
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder={isConnected ? "Type your message..." : "Connecting..."}
              disabled={!isConnected}
              className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg 
                       bg-white dark:bg-gray-800 text-text placeholder-gray-500 
                       focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent
                       disabled:opacity-50 disabled:cursor-not-allowed
                       resize-none min-h-[50px] max-h-[120px]"
              rows={1}
            />
          </div>
          <motion.button
            type="submit"
            disabled={!inputMessage.trim() || !isConnected}
            className="px-6 py-3 bg-primary text-white rounded-lg font-medium
                     hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2
                     disabled:opacity-50 disabled:cursor-not-allowed
                     flex items-center space-x-2"
            whileHover={animationConfig.enableHover ? { scale: 1.05 } : {}}
            whileTap={animationConfig.level !== AnimationLevels.NONE ? { scale: 0.95 } : {}}
          >
            {isTyping ? (
              <Loader className="w-5 h-5 animate-spin" />
            ) : (
              <Send className="w-5 h-5" />
            )}
            <span className="hidden sm:inline">Send</span>
          </motion.button>
        </form>
      </div>
    </div>
  );
};

export default ChatInterface;