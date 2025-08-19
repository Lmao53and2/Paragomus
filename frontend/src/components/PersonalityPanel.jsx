import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Brain, 
  User, 
  Settings, 
  TrendingUp, 
  Eye,
  EyeOff,
  ChevronDown,
  ChevronUp,
  Palette,
  MessageSquare,
  Target
} from 'lucide-react';
import { PersonalityTraits, AnimationLevels } from '../types';

const PersonalityPanel = ({ 
  personalityProfile, 
  adaptations, 
  config, 
  animationConfig 
}) => {
  const [isExpanded, setIsExpanded] = useState(!config.compact);
  const [activeTab, setActiveTab] = useState('traits');

  // Get trait value with fallback
  const getTraitValue = (trait) => {
    return personalityProfile.traits?.[trait] || 0.5;
  };

  // Get confidence score
  const getConfidenceScore = (category) => {
    return personalityProfile.confidence_scores?.[category] || 0;
  };

  // Format trait name for display
  const formatTraitName = (trait) => {
    return trait.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
  };

  // Get trait color based on value
  const getTraitColor = (value) => {
    if (value >= 0.7) return 'bg-green-500';
    if (value >= 0.4) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  // Render trait bar
  const renderTraitBar = (trait, value) => (
    <div key={trait} className="space-y-2">
      <div className="flex justify-between items-center">
        <span className="text-sm font-medium text-text">{formatTraitName(trait)}</span>
        <span className="text-xs text-gray-500">{Math.round(value * 100)}%</span>
      </div>
      <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
        <motion.div
          className={`h-2 rounded-full ${getTraitColor(value)}`}
          initial={{ width: 0 }}
          animate={{ width: `${value * 100}%` }}
          transition={{ 
            duration: animationConfig.level === AnimationLevels.NONE ? 0 : 0.8,
            ease: 'easeOut'
          }}
        />
      </div>
    </div>
  );

  // Render preferences
  const renderPreferences = () => (
    <div className="space-y-3">
      {Object.entries(personalityProfile.preferences || {}).map(([key, value]) => (
        <div key={key} className="flex justify-between items-center py-2 border-b border-gray-100 dark:border-gray-700">
          <span className="text-sm font-medium text-text">{formatTraitName(key)}</span>
          <span className="text-sm text-gray-600 dark:text-gray-400 capitalize">{value}</span>
        </div>
      ))}
    </div>
  );

  // Render adaptations
  const renderAdaptations = () => (
    <div className="space-y-4">
      {Object.entries(adaptations).map(([agentType, agentAdaptations]) => (
        <div key={agentType} className="space-y-2">
          <h4 className="text-sm font-semibold text-text flex items-center space-x-2">
            {agentType.includes('chat') && <MessageSquare className="w-4 h-4" />}
            {agentType.includes('task') && <Target className="w-4 h-4" />}
            {agentType.includes('ui') && <Palette className="w-4 h-4" />}
            <span>{formatTraitName(agentType.replace('_adaptations', ''))}</span>
          </h4>
          <div className="bg-gray-50 dark:bg-gray-800 rounded-lg p-3 space-y-1">
            {Object.entries(agentAdaptations).map(([key, value]) => (
              <div key={key} className="flex justify-between text-xs">
                <span className="text-gray-600 dark:text-gray-400">{formatTraitName(key)}:</span>
                <span className="text-text font-medium capitalize">{value}</span>
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );

  // Animation variants
  const panelVariants = {
    hidden: { 
      opacity: 0, 
      scale: config.compact ? 0.9 : 1,
      y: config.compact ? 20 : 0
    },
    visible: { 
      opacity: 1, 
      scale: 1,
      y: 0,
      transition: {
        duration: animationConfig.level === AnimationLevels.NONE ? 0 : 0.3
      }
    }
  };

  const contentVariants = {
    hidden: { opacity: 0, height: 0 },
    visible: { 
      opacity: 1, 
      height: 'auto',
      transition: {
        duration: animationConfig.level === AnimationLevels.NONE ? 0 : 0.3,
        ease: 'easeInOut'
      }
    }
  };

  // Tab configuration
  const tabs = [
    { id: 'traits', label: 'Traits', icon: Brain },
    { id: 'preferences', label: 'Preferences', icon: Settings },
    { id: 'adaptations', label: 'Adaptations', icon: TrendingUp }
  ];

  return (
    <motion.div
      className={`bg-white dark:bg-gray-900 rounded-lg shadow-lg overflow-hidden ${
        config.compact ? 'w-80' : 'w-full'
      }`}
      variants={panelVariants}
      initial="hidden"
      animate="visible"
    >
      {/* Header */}
      <div className="bg-gradient-to-r from-purple-500 to-pink-500 text-white px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <User className="w-6 h-6" />
            <h2 className="text-lg font-semibold">Personality Profile</h2>
          </div>
          {config.compact && (
            <button
              onClick={() => setIsExpanded(!isExpanded)}
              className="text-white hover:text-gray-200 transition-colors"
            >
              {isExpanded ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
            </button>
          )}
        </div>
        
        {/* Confidence indicator */}
        <div className="mt-3 flex items-center space-x-2">
          <span className="text-sm opacity-90">Confidence:</span>
          <div className="flex-1 bg-white/20 rounded-full h-2">
            <div 
              className="bg-white h-2 rounded-full transition-all duration-500"
              style={{ width: `${getConfidenceScore('traits') * 100}%` }}
            />
          </div>
          <span className="text-sm opacity-90">
            {Math.round(getConfidenceScore('traits') * 100)}%
          </span>
        </div>
      </div>

      {/* Content */}
      <AnimatePresence>
        {(isExpanded || !config.compact) && (
          <motion.div
            variants={contentVariants}
            initial="hidden"
            animate="visible"
            exit="hidden"
          >
            {/* Tabs */}
            {config.detailLevel !== 'summary' && (
              <div className="border-b border-gray-200 dark:border-gray-700">
                <div className="flex">
                  {tabs.map(({ id, label, icon: Icon }) => (
                    <button
                      key={id}
                      onClick={() => setActiveTab(id)}
                      className={`flex-1 flex items-center justify-center space-x-2 py-3 px-4 text-sm font-medium transition-colors ${
                        activeTab === id
                          ? 'text-primary border-b-2 border-primary bg-primary/5'
                          : 'text-gray-500 hover:text-gray-700 dark:hover:text-gray-300'
                      }`}
                    >
                      <Icon className="w-4 h-4" />
                      <span className="hidden sm:inline">{label}</span>
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* Tab Content */}
            <div className="p-6">
              <AnimatePresence mode="wait">
                {(activeTab === 'traits' || config.detailLevel === 'summary') && (
                  <motion.div
                    key="traits"
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0, x: 20 }}
                    transition={{ duration: animationConfig.level === AnimationLevels.NONE ? 0 : 0.2 }}
                    className="space-y-4"
                  >
                    <h3 className="text-sm font-semibold text-text mb-4">Personality Traits</h3>
                    {Object.entries(PersonalityTraits).map(([key, trait]) => 
                      renderTraitBar(trait, getTraitValue(trait))
                    )}
                  </motion.div>
                )}

                {activeTab === 'preferences' && config.detailLevel !== 'summary' && (
                  <motion.div
                    key="preferences"
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0, x: 20 }}
                    transition={{ duration: animationConfig.level === AnimationLevels.NONE ? 0 : 0.2 }}
                  >
                    <h3 className="text-sm font-semibold text-text mb-4">Communication Preferences</h3>
                    {renderPreferences()}
                  </motion.div>
                )}

                {activeTab === 'adaptations' && config.detailLevel !== 'summary' && (
                  <motion.div
                    key="adaptations"
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0, x: 20 }}
                    transition={{ duration: animationConfig.level === AnimationLevels.NONE ? 0 : 0.2 }}
                  >
                    <h3 className="text-sm font-semibold text-text mb-4">Active Adaptations</h3>
                    {renderAdaptations()}
                  </motion.div>
                )}
              </AnimatePresence>
            </div>

            {/* Footer */}
            {personalityProfile.interaction_history && personalityProfile.interaction_history.length > 0 && (
              <div className="bg-gray-50 dark:bg-gray-800 px-6 py-3 border-t border-gray-200 dark:border-gray-700">
                <div className="flex items-center justify-between text-sm text-gray-600 dark:text-gray-400">
                  <span>Interactions: {personalityProfile.interaction_history.length}</span>
                  <span>Last updated: {new Date().toLocaleTimeString()}</span>
                </div>
              </div>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
};

export default PersonalityPanel;