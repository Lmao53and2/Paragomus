import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  CheckSquare, 
  Square, 
  Clock, 
  AlertCircle, 
  Calendar,
  Filter,
  Grid,
  List,
  Kanban
} from 'lucide-react';
import { TaskPriorities, TaskStatuses, AnimationLevels } from '../types';

const TaskPanel = ({ tasks, config, animationConfig, onTaskUpdate }) => {
  const [filter, setFilter] = useState('all');
  const [viewType, setViewType] = useState(config.viewType || 'list');

  // Filter tasks based on current filter
  const filteredTasks = tasks.filter(task => {
    switch (filter) {
      case 'completed':
        return task.status === TaskStatuses.COMPLETED;
      case 'pending':
        return task.status === TaskStatuses.TODO || task.status === TaskStatuses.IN_PROGRESS;
      case 'high-priority':
        return task.priority === TaskPriorities.HIGH;
      default:
        return true;
    }
  });

  // Group tasks by category or priority
  const groupedTasks = filteredTasks.reduce((groups, task) => {
    const key = config.groupBy === 'category' ? task.category || 'Other' :
                config.groupBy === 'priority' ? task.priority || 'medium' :
                config.groupBy === 'date' ? task.due_date || 'No date' : 'all';
    
    if (!groups[key]) {
      groups[key] = [];
    }
    groups[key].push(task);
    return groups;
  }, {});

  // Handle task status toggle
  const handleTaskToggle = (task) => {
    const newStatus = task.status === TaskStatuses.COMPLETED 
      ? TaskStatuses.TODO 
      : TaskStatuses.COMPLETED;
    
    onTaskUpdate({ ...task, status: newStatus });
  };

  // Get priority color
  const getPriorityColor = (priority) => {
    switch (priority) {
      case TaskPriorities.HIGH:
        return 'text-red-500 bg-red-50 dark:bg-red-900/20';
      case TaskPriorities.MEDIUM:
        return 'text-yellow-500 bg-yellow-50 dark:bg-yellow-900/20';
      case TaskPriorities.LOW:
        return 'text-green-500 bg-green-50 dark:bg-green-900/20';
      default:
        return 'text-gray-500 bg-gray-50 dark:bg-gray-800';
    }
  };

  // Get priority icon
  const getPriorityIcon = (priority) => {
    switch (priority) {
      case TaskPriorities.HIGH:
        return <AlertCircle className="w-4 h-4" />;
      case TaskPriorities.MEDIUM:
        return <Clock className="w-4 h-4" />;
      default:
        return <Calendar className="w-4 h-4" />;
    }
  };

  // Animation variants
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: animationConfig.level === AnimationLevels.FULL ? 0.1 : 0
      }
    }
  };

  const taskVariants = {
    hidden: { 
      opacity: 0, 
      x: -20,
      scale: animationConfig.level === AnimationLevels.FULL ? 0.95 : 1
    },
    visible: { 
      opacity: 1, 
      x: 0,
      scale: 1,
      transition: {
        duration: animationConfig.level === AnimationLevels.NONE ? 0 : 0.3
      }
    },
    exit: {
      opacity: 0,
      x: 20,
      scale: 0.95,
      transition: { duration: 0.2 }
    }
  };

  // Render task item
  const renderTask = (task) => (
    <motion.div
      key={task.id}
      className={`p-4 bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700
                 hover:shadow-md transition-shadow cursor-pointer
                 ${task.status === TaskStatuses.COMPLETED ? 'opacity-60' : ''}`}
      variants={taskVariants}
      layout={animationConfig.level === AnimationLevels.FULL}
      whileHover={animationConfig.enableHover ? { y: -2 } : {}}
      onClick={() => handleTaskToggle(task)}
    >
      <div className="flex items-start space-x-3">
        <button
          className="mt-1 text-primary hover:text-primary/80"
          onClick={(e) => {
            e.stopPropagation();
            handleTaskToggle(task);
          }}
        >
          {task.status === TaskStatuses.COMPLETED ? (
            <CheckSquare className="w-5 h-5" />
          ) : (
            <Square className="w-5 h-5" />
          )}
        </button>
        
        <div className="flex-1 min-w-0">
          <h4 className={`font-medium text-sm ${
            task.status === TaskStatuses.COMPLETED ? 'line-through text-gray-500' : 'text-text'
          }`}>
            {task.title}
          </h4>
          
          {task.description && (
            <p className="text-xs text-gray-600 dark:text-gray-400 mt-1 line-clamp-2">
              {task.description}
            </p>
          )}
          
          <div className="flex items-center justify-between mt-3">
            {config.showPriority && task.priority && (
              <div className={`flex items-center space-x-1 px-2 py-1 rounded-full text-xs ${getPriorityColor(task.priority)}`}>
                {getPriorityIcon(task.priority)}
                <span className="capitalize">{task.priority}</span>
              </div>
            )}
            
            {config.showDeadlines && task.due_date && (
              <div className="flex items-center space-x-1 text-xs text-gray-500">
                <Calendar className="w-3 h-3" />
                <span>{task.due_date}</span>
              </div>
            )}
            
            {task.estimated_time && (
              <div className="flex items-center space-x-1 text-xs text-gray-500">
                <Clock className="w-3 h-3" />
                <span>{task.estimated_time}</span>
              </div>
            )}
          </div>
          
          {task.subtasks && task.subtasks.length > 0 && (
            <div className="mt-2 space-y-1">
              {task.subtasks.slice(0, 2).map((subtask, index) => (
                <div key={index} className="text-xs text-gray-600 dark:text-gray-400 flex items-center space-x-1">
                  <div className="w-1 h-1 bg-gray-400 rounded-full" />
                  <span>{subtask}</span>
                </div>
              ))}
              {task.subtasks.length > 2 && (
                <div className="text-xs text-gray-500">
                  +{task.subtasks.length - 2} more
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </motion.div>
  );

  // Render view type selector
  const renderViewSelector = () => (
    <div className="flex items-center space-x-1 bg-gray-100 dark:bg-gray-800 rounded-lg p-1">
      {[
        { type: 'list', icon: List },
        { type: 'grid', icon: Grid },
        { type: 'kanban', icon: Kanban }
      ].map(({ type, icon: Icon }) => (
        <button
          key={type}
          onClick={() => setViewType(type)}
          className={`p-2 rounded-md transition-colors ${
            viewType === type
              ? 'bg-white dark:bg-gray-700 text-primary shadow-sm'
              : 'text-gray-500 hover:text-gray-700 dark:hover:text-gray-300'
          }`}
        >
          <Icon className="w-4 h-4" />
        </button>
      ))}
    </div>
  );

  return (
    <div className="bg-white dark:bg-gray-900 rounded-lg shadow-lg overflow-hidden">
      {/* Header */}
      <div className="bg-gray-50 dark:bg-gray-800 px-6 py-4 border-b border-gray-200 dark:border-gray-700">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-semibold text-text">Tasks</h2>
          <div className="flex items-center space-x-3">
            {renderViewSelector()}
            <div className="relative">
              <select
                value={filter}
                onChange={(e) => setFilter(e.target.value)}
                className="appearance-none bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 
                         rounded-md px-3 py-1 text-sm text-text focus:outline-none focus:ring-2 focus:ring-primary"
              >
                <option value="all">All Tasks</option>
                <option value="pending">Pending</option>
                <option value="completed">Completed</option>
                <option value="high-priority">High Priority</option>
              </select>
              <Filter className="w-4 h-4 absolute right-2 top-1/2 transform -translate-y-1/2 text-gray-400 pointer-events-none" />
            </div>
          </div>
        </div>
        
        {/* Stats */}
        <div className="flex items-center space-x-4 mt-3 text-sm text-gray-600 dark:text-gray-400">
          <span>{tasks.length} total</span>
          <span>{tasks.filter(t => t.status === TaskStatuses.COMPLETED).length} completed</span>
          <span>{tasks.filter(t => t.priority === TaskPriorities.HIGH).length} high priority</span>
        </div>
      </div>

      {/* Tasks */}
      <div className="p-6 max-h-[500px] overflow-y-auto scrollbar-thin">
        {filteredTasks.length === 0 ? (
          <div className="text-center py-12">
            <CheckSquare className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-500 dark:text-gray-400">
              {filter === 'all' ? 'No tasks yet' : `No ${filter} tasks`}
            </p>
          </div>
        ) : (
          <motion.div
            variants={containerVariants}
            initial="hidden"
            animate="visible"
          >
            <AnimatePresence>
              {config.groupBy && config.groupBy !== 'all' ? (
                // Grouped view
                Object.entries(groupedTasks).map(([group, groupTasks]) => (
                  <div key={group} className="mb-6">
                    <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-3 capitalize">
                      {group} ({groupTasks.length})
                    </h3>
                    <div className={`space-y-3 ${viewType === 'grid' ? 'grid grid-cols-1 sm:grid-cols-2 gap-3' : ''}`}>
                      {groupTasks.map(renderTask)}
                    </div>
                  </div>
                ))
              ) : (
                // Simple list view
                <div className={`${viewType === 'grid' ? 'grid grid-cols-1 sm:grid-cols-2 gap-3' : 'space-y-3'}`}>
                  {filteredTasks.map(renderTask)}
                </div>
              )}
            </AnimatePresence>
          </motion.div>
        )}
      </div>
    </div>
  );
};

export default TaskPanel;