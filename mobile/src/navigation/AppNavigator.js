/**
 * Main app navigation — handles auth state and tab navigation.
 */
import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { ActivityIndicator, View } from 'react-native';
import { useAuth } from '../contexts/AuthContext';

import LoginScreen from '../screens/LoginScreen';
import ChatListScreen from '../screens/ChatListScreen';
import ChatScreen from '../screens/ChatScreen';
import HistoryScreen from '../screens/HistoryScreen';
import AdminDashboardScreen from '../screens/AdminDashboardScreen';
import AdminDocumentsScreen from '../screens/AdminDocumentsScreen';
import AdminUsersScreen from '../screens/AdminUsersScreen';
import AdminLogsScreen from '../screens/AdminLogsScreen';

const Stack = createNativeStackNavigator();
const Tab = createBottomTabNavigator();

function UserTabs() {
  return (
    <Tab.Navigator screenOptions={{ headerShown: false }}>
      <Tab.Screen name="Conversas" component={ChatStackNavigator} />
      <Tab.Screen name="Histórico" component={HistoryScreen} />
    </Tab.Navigator>
  );
}

function AdminTabs() {
  return (
    <Tab.Navigator screenOptions={{ headerShown: false }}>
      <Tab.Screen name="Conversas" component={ChatStackNavigator} />
      <Tab.Screen name="Histórico" component={HistoryScreen} />
      <Tab.Screen name="Painel" component={AdminStackNavigator} />
    </Tab.Navigator>
  );
}

function ChatStackNavigator() {
  return (
    <Stack.Navigator>
      <Stack.Screen name="ChatList" component={ChatListScreen} options={{ title: 'Minhas Conversas' }} />
      <Stack.Screen name="Chat" component={ChatScreen} options={{ title: 'Chat' }} />
    </Stack.Navigator>
  );
}

function AdminStackNavigator() {
  return (
    <Stack.Navigator>
      <Stack.Screen name="AdminDashboard" component={AdminDashboardScreen} options={{ title: 'Administração' }} />
      <Stack.Screen name="AdminDocuments" component={AdminDocumentsScreen} options={{ title: 'Documentos' }} />
      <Stack.Screen name="AdminUsers" component={AdminUsersScreen} options={{ title: 'Usuários' }} />
      <Stack.Screen name="AdminLogs" component={AdminLogsScreen} options={{ title: 'Logs' }} />
    </Stack.Navigator>
  );
}

export default function AppNavigator() {
  const { user, loading, isAdmin } = useAuth();

  if (loading) {
    return (
      <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
        <ActivityIndicator size="large" color="#1a73e8" />
      </View>
    );
  }

  return (
    <NavigationContainer>
      <Stack.Navigator screenOptions={{ headerShown: false }}>
        {!user ? (
          <Stack.Screen name="Login" component={LoginScreen} />
        ) : isAdmin ? (
          <Stack.Screen name="AdminTabs" component={AdminTabs} />
        ) : (
          <Stack.Screen name="UserTabs" component={UserTabs} />
        )}
      </Stack.Navigator>
    </NavigationContainer>
  );
}
