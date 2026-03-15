/**
 * History screen — shows all conversations with their messages.
 */
import React, { useState, useCallback } from 'react';
import { View, Text, FlatList, TouchableOpacity, StyleSheet, Alert } from 'react-native';
import { useFocusEffect } from '@react-navigation/native';
import { listConversas } from '../services/chatService';

export default function HistoryScreen({ navigation }) {
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
      Alert.alert('Erro', 'Não foi possível carregar o histórico');
    }
  }

  function renderItem({ item }) {
    return (
      <TouchableOpacity
        style={styles.card}
        onPress={() => navigation.navigate('Conversas', {
          screen: 'Chat',
          params: { conversaId: item.id, titulo: item.titulo },
        })}
      >
        <Text style={styles.cardTitle}>{item.titulo || 'Sem título'}</Text>
        <Text style={styles.cardDate}>
          Criado em: {new Date(item.criado_em).toLocaleDateString('pt-BR')}
        </Text>
        <Text style={styles.cardDate}>
          Atualizado em: {new Date(item.atualizado_em).toLocaleDateString('pt-BR')}
        </Text>
      </TouchableOpacity>
    );
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Histórico de Conversas</Text>
      <FlatList
        data={conversas}
        keyExtractor={(item) => String(item.id)}
        renderItem={renderItem}
        ListEmptyComponent={<Text style={styles.empty}>Nenhuma conversa no histórico</Text>}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f5f5f5', paddingTop: 48 },
  title: { fontSize: 20, fontWeight: 'bold', color: '#333', padding: 16 },
  card: {
    backgroundColor: '#fff', marginHorizontal: 16, marginVertical: 6,
    padding: 16, borderRadius: 8, elevation: 1,
  },
  cardTitle: { fontSize: 16, fontWeight: '500', color: '#333' },
  cardDate: { fontSize: 12, color: '#999', marginTop: 2 },
  empty: { textAlign: 'center', color: '#999', marginTop: 40 },
});
