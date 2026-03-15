/**
 * Chat list screen — shows all conversations and allows creating new ones.
 */
import React, { useState, useCallback } from 'react';
import { View, Text, FlatList, TouchableOpacity, StyleSheet, Alert } from 'react-native';
import { useFocusEffect } from '@react-navigation/native';
import { listConversas, createConversa } from '../services/chatService';
import { useAuth } from '../contexts/AuthContext';

export default function ChatListScreen({ navigation }) {
  const { logout } = useAuth();
  const [conversas, setConversas] = useState([]);

  useFocusEffect(
    useCallback(() => {
      loadConversas();
    }, [])
  );

  async function loadConversas() {
    try {
      const data = await listConversas();
      setConversas(data);
    } catch {
      Alert.alert('Erro', 'Não foi possível carregar conversas');
    }
  }

  async function handleNewConversa() {
    try {
      const conversa = await createConversa('Nova conversa');
      navigation.navigate('Chat', { conversaId: conversa.id, titulo: conversa.titulo });
    } catch {
      Alert.alert('Erro', 'Não foi possível criar conversa');
    }
  }

  function renderItem({ item }) {
    return (
      <TouchableOpacity
        style={styles.card}
        onPress={() => navigation.navigate('Chat', { conversaId: item.id, titulo: item.titulo })}
      >
        <Text style={styles.cardTitle}>{item.titulo || 'Sem título'}</Text>
        <Text style={styles.cardDate}>
          {new Date(item.criado_em).toLocaleDateString('pt-BR')}
        </Text>
      </TouchableOpacity>
    );
  }

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Minhas Conversas</Text>
        <TouchableOpacity onPress={logout}>
          <Text style={styles.logoutText}>Sair</Text>
        </TouchableOpacity>
      </View>

      <FlatList
        data={conversas}
        keyExtractor={(item) => String(item.id)}
        renderItem={renderItem}
        ListEmptyComponent={<Text style={styles.empty}>Nenhuma conversa ainda</Text>}
      />

      <TouchableOpacity style={styles.fab} onPress={handleNewConversa}>
        <Text style={styles.fabText}>+</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f5f5f5' },
  header: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', padding: 16, paddingTop: 48 },
  title: { fontSize: 20, fontWeight: 'bold', color: '#333' },
  logoutText: { color: '#e53935', fontSize: 14 },
  card: {
    backgroundColor: '#fff', marginHorizontal: 16, marginVertical: 6,
    padding: 16, borderRadius: 8, elevation: 1,
  },
  cardTitle: { fontSize: 16, fontWeight: '500', color: '#333' },
  cardDate: { fontSize: 12, color: '#999', marginTop: 4 },
  empty: { textAlign: 'center', color: '#999', marginTop: 40 },
  fab: {
    position: 'absolute', right: 24, bottom: 24,
    width: 56, height: 56, borderRadius: 28,
    backgroundColor: '#1a73e8', justifyContent: 'center', alignItems: 'center',
    elevation: 4,
  },
  fabText: { color: '#fff', fontSize: 28, lineHeight: 28 },
});
