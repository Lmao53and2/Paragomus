// Type definitions for the adaptive AI assistant

export const PersonalityTraits = {
  OPENNESS: 'openness',
  CONSCIENTIOUSNESS: 'conscientiousness',
  EXTRAVERSION: 'extraversion',
  AGREEABLENESS: 'agreeableness',
  NEUROTICISM: 'neuroticism',
  COMMUNICATION_DIRECTNESS: 'communication_directness',
  TECHNICAL_APTITUDE: 'technical_aptitude'
};

export const UIThemes = {
  LIGHT: 'light',
  DARK: 'dark',
  AUTO: 'auto',
  MINIMAL: 'minimal'
};

export const LayoutTypes = {
  MINIMAL: 'minimal',
  STANDARD: 'standard',
  DETAILED: 'detailed'
};

export const AnimationLevels = {
  NONE: 'none',
  SUBTLE: 'subtle',
  FULL: 'full'
};

export const MessageTypes = {
  USER: 'user',
  ASSISTANT: 'assistant',
  SYSTEM: 'system'
};

export const TaskPriorities = {
  LOW: 'low',
  MEDIUM: 'medium',
  HIGH: 'high'
};

export const TaskStatuses = {
  TODO: 'todo',
  IN_PROGRESS: 'in_progress',
  COMPLETED: 'completed',
  CANCELLED: 'cancelled'
};