/**
 * Admin logs screen — shows admin activity log entries.
 */
import React, { useState, useCallback } from 'react';
import { View, Text, FlatList, StyleSheet, Alert } from 'react-native';
import { useFocusEffect } from '@react-navigation/native';
import { getLogs } from '../services/adminService';

export default function AdminLogsScreen() {
  const [logs, setLogs] = useState([]);

  useFocusEffect(
    useCallback(() => {
      loadLogs();
    }, [])
  );

  async function loadLogs() {
    try {
      const data = await getLogs();
      setLogs(data);
    } catch {
      Alert.alert('Erro', 'Não foi possível carregar os logs');
    }
  }

  function renderItem({ item }) {
    return (
      <View style={styles.card}>
        <View style={styles.header}>
          <Text style={styles.action}>{item.acao}</Text>
          <Text style={styles.date}>
            {new Date(item.criado_em).toLocaleString('pt-BR')}
          </Text>
        </View>
        {item.entidade && (
          <Text style={styles.detail}>
            {item.entidade} #{item.entidade_id}
          </Text>
        )}
        {item.detalhes && <Text style={styles.detail}>{item.detalhes}</Text>}
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <FlatList
        data={logs}
        keyExtractor={(item) => String(item.id)}
        renderItem={renderItem}
        ListEmptyComponent={<Text style={styles.empty}>Nenhum log registrado</Text>}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f5f5f5' },
  card: {
    backgroundColor: '#fff', marginHorizontal: 16, marginVertical: 4,
    padding: 12, borderRadius: 8, elevation: 1,
  },
  header: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' },
  action: { fontSize: 14, fontWeight: '600', color: '#1a73e8' },
  date: { fontSize: 11, color: '#999' },
  detail: { fontSize: 13, color: '#666', marginTop: 4 },
  empty: { textAlign: 'center', color: '#999', marginTop: 40 },
});
