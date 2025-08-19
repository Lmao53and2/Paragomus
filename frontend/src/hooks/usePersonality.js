import { useState, useEffect, useCallback } from 'react';
import { apiService } from '../services/api';

export const usePersonality = () => {
  const [personalityProfile, setPersonalityProfile] = useState({});
  const [adaptations, setAdaptations] = useState({});
  const [uiConfig, setUIConfig] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Load initial personality data
  const loadPersonalityData = useCallback(async () => {
    setLoading(true);
    setError(null);
    
    try {
      const [profile, adaptationsData, uiConfigData] = await Promise.all([
        apiService.getPersonalityProfile(),
        apiService.getAdaptations(),
        apiService.getUIConfig()
      ]);

      setPersonalityProfile(profile);
      setAdaptations(adaptationsData);
      setUIConfig(uiConfigData);
    } catch (err) {
      setError(err.message);
      console.error('Failed to load personality data:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  // Update personality profile
  const updatePersonalityProfile = useCallback((newProfile) => {
    setPersonalityProfile(prev => ({
      ...prev,
      ...newProfile
    }));
  }, []);

  // Update adaptations
  const updateAdaptations = useCallback((newAdaptations) => {
    setAdaptations(prev => ({
      ...prev,
      ...newAdaptations
    }));
  }, []);

  // Update UI config
  const updateUIConfig = useCallback((newConfig) => {
    setUIConfig(prev => ({
      ...prev,
      ...newConfig
    }));
  }, []);

  // Get personality trait value
  const getTraitValue = useCallback((trait) => {
    return personalityProfile.traits?.[trait] || 0.5;
  }, [personalityProfile]);

  // Get preference value
  const getPreference = useCallback((preference) => {
    return personalityProfile.preferences?.[preference] || null;
  }, [personalityProfile]);

  // Get communication style
  const getCommunicationStyle = useCallback((style) => {
    return personalityProfile.communication_style?.[style] || null;
  }, [personalityProfile]);

  // Get UI preference
  const getUIPreference = useCallback((preference) => {
    return personalityProfile.ui_preferences?.[preference] || null;
  }, [personalityProfile]);

  // Check if personality data is available
  const hasPersonalityData = useCallback(() => {
    return Object.keys(personalityProfile).length > 0;
  }, [personalityProfile]);

  // Get confidence score for a category
  const getConfidenceScore = useCallback((category) => {
    return personalityProfile.confidence_scores?.[category] || 0;
  }, [personalityProfile]);

  // Get adaptation suggestion
  const getAdaptationSuggestion = useCallback((agent, suggestion) => {
    return adaptations[`${agent}_adaptations`]?.[suggestion] || null;
  }, [adaptations]);

  // Get theme configuration
  const getThemeConfig = useCallback(() => {
    return uiConfig.theme || {};
  }, [uiConfig]);

  // Get layout configuration
  const getLayoutConfig = useCallback(() => {
    return uiConfig.layout || {};
  }, [uiConfig]);

  // Get component configuration
  const getComponentConfig = useCallback((component) => {
    return uiConfig.components?.[component] || {};
  }, [uiConfig]);

  // Get animation configuration
  const getAnimationConfig = useCallback(() => {
    return uiConfig.animations || {};
  }, [uiConfig]);

  // Apply theme to document
  const applyTheme = useCallback(() => {
    const theme = getThemeConfig();
    const root = document.documentElement;
    
    if (theme.colorScheme) {
      root.setAttribute('data-theme', theme.colorScheme);
    }
    
    if (theme.primaryColor) {
      root.style.setProperty('--color-primary', theme.primaryColor);
    }
    
    if (theme.secondaryColor) {
      root.style.setProperty('--color-secondary', theme.secondaryColor);
    }
    
    if (theme.accentColor) {
      root.style.setProperty('--color-accent', theme.accentColor);
    }
    
    if (theme.backgroundColor) {
      root.style.setProperty('--color-background', theme.backgroundColor);
    }
    
    if (theme.textColor) {
      root.style.setProperty('--color-text', theme.textColor);
    }
  }, [getThemeConfig]);

  // Load data on mount
  useEffect(() => {
    loadPersonalityData();
  }, [loadPersonalityData]);

  // Apply theme when UI config changes
  useEffect(() => {
    if (Object.keys(uiConfig).length > 0) {
      applyTheme();
    }
  }, [uiConfig, applyTheme]);

  return {
    // State
    personalityProfile,
    adaptations,
    uiConfig,
    loading,
    error,
    
    // Actions
    loadPersonalityData,
    updatePersonalityProfile,
    updateAdaptations,
    updateUIConfig,
    
    // Getters
    getTraitValue,
    getPreference,
    getCommunicationStyle,
    getUIPreference,
    hasPersonalityData,
    getConfidenceScore,
    getAdaptationSuggestion,
    getThemeConfig,
    getLayoutConfig,
    getComponentConfig,
    getAnimationConfig,
    
    // Utilities
    applyTheme
  };
};