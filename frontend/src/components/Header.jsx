import React from 'react';
import { motion } from 'framer-motion';
import { Brain, Wifi, WifiOff, Settings, User } from 'lucide-react';

const Header = ({ isConnected, connectionError, personalityProfile, layoutConfig }) => {
  // Get user's primary trait for display
  const getPrimaryTrait = () => {
    if (!personalityProfile.traits) return null;
    
    const traits = personalityProfile.traits;
    const maxTrait = Object.entries(traits).reduce((max, [key, value]) => 
      value > max.value ? { key, value } : max, { key: '', value: 0 }
    );
    
    return maxTrait.value > 0 ? maxTrait.key : null;
  };

  const primaryTrait = getPrimaryTrait();

  return (
    <motion.header
      className="bg-white dark:bg-gray-900 shadow-sm border-b border-gray-200 dark:border-gray-700"
      initial={{ y: -50, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.3 }}
    >
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          {/* Logo and Title */}
          <div className="flex items-center space-x-4">
            <motion.div
              className="flex items-center space-x-3"
              whileHover={{ scale: 1.05 }}
              transition={{ duration: 0.2 }}
            >
              <div className="p-2 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg">
                <Brain className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-text">Adaptive AI Assistant</h1>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Personalized Intelligence
                </p>
              </div>
            </motion.div>
          </div>

          {/* Status and Info */}
          <div className="flex items-center space-x-6">
            {/* Personality Indicator */}
            {primaryTrait && (
              <motion.div
                className="hidden md:flex items-center space-x-2 px-3 py-2 bg-purple-50 dark:bg-purple-900/20 rounded-lg"
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ delay: 0.5, duration: 0.3 }}
              >
                <User className="w-4 h-4 text-purple-600 dark:text-purple-400" />
                <span className="text-sm font-medium text-purple-700 dark:text-purple-300 capitalize">
                  {primaryTrait.replace(/_/g, ' ')}
                </span>
              </motion.div>
            )}

            {/* Layout Indicator */}
            <div className="hidden sm:flex items-center space-x-2 text-sm text-gray-600 dark:text-gray-400">
              <Settings className="w-4 h-4" />
              <span className="capitalize">{layoutConfig.type || 'standard'} Layout</span>
            </div>

            {/* Connection Status */}
            <motion.div
              className="flex items-center space-x-2"
              animate={{ 
                scale: isConnected ? 1 : [1, 1.1, 1],
                transition: { 
                  repeat: isConnected ? 0 : Infinity,
                  duration: 1.5 
                }
              }}
            >
              {isConnected ? (
                <>
                  <Wifi className="w-5 h-5 text-green-500" />
                  <span className="text-sm font-medium text-green-600 dark:text-green-400">
                    Connected
                  </span>
                </>
              ) : (
                <>
                  <WifiOff className="w-5 h-5 text-red-500" />
                  <span className="text-sm font-medium text-red-600 dark:text-red-400">
                    {connectionError ? 'Error' : 'Connecting...'}
                  </span>
                </>
              )}
            </motion.div>
          </div>
        </div>

        {/* Error Message */}
        {connectionError && (
          <motion.div
            className="mt-3 p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg"
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            transition={{ duration: 0.3 }}
          >
            <p className="text-sm text-red-700 dark:text-red-300">
              Connection Error: {connectionError.message}
            </p>
          </motion.div>
        )}
      </div>
    </motion.header>
  );
};

export default Header;