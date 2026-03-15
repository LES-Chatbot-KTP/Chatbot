/**
 * Admin users screen — list and create users.
 */
import React, { useState, useCallback } from 'react';
import {
  View, Text, FlatList, TouchableOpacity, TextInput, StyleSheet, Alert, Modal,
} from 'react-native';
import { useFocusEffect } from '@react-navigation/native';
import { listUsuarios, createUsuario } from '../services/adminService';

export default function AdminUsersScreen() {
  const [usuarios, setUsuarios] = useState([]);
  const [modalVisible, setModalVisible] = useState(false);
  const [nome, setNome] = useState('');
  const [email, setEmail] = useState('');
  const [senha, setSenha] = useState('');

  useFocusEffect(
    useCallback(() => {
      loadUsuarios();
    }, [])
  );

  async function loadUsuarios() {
    try {
      const data = await listUsuarios();
      setUsuarios(data);
    } catch {
      Alert.alert('Erro', 'Não foi possível carregar usuários');
    }
  }

  async function handleCreate() {
    if (!nome || !email || !senha) {
      Alert.alert('Erro', 'Preencha todos os campos');
      return;
    }
    try {
      await createUsuario({ nome, email, senha, perfil_id: 2 });
      setNome('');
      setEmail('');
      setSenha('');
      setModalVisible(false);
      loadUsuarios();
      Alert.alert('Sucesso', 'Usuário criado');
    } catch {
      Alert.alert('Erro', 'Não foi possível criar usuário');
    }
  }

  function renderItem({ item }) {
    return (
      <View style={styles.card}>
        <Text style={styles.cardName}>{item.nome}</Text>
        <Text style={styles.cardEmail}>{item.email}</Text>
        <Text style={[styles.cardStatus, { color: item.ativo ? '#4caf50' : '#e53935' }]}>
          {item.ativo ? 'Ativo' : 'Inativo'}
        </Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <FlatList
        data={usuarios}
        keyExtractor={(item) => String(item.id)}
        renderItem={renderItem}
        ListEmptyComponent={<Text style={styles.empty}>Nenhum usuário</Text>}
      />

      <TouchableOpacity style={styles.fab} onPress={() => setModalVisible(true)}>
        <Text style={styles.fabText}>+</Text>
      </TouchableOpacity>

      <Modal visible={modalVisible} animationType="slide" transparent>
        <View style={styles.modalOverlay}>
          <View style={styles.modalContent}>
            <Text style={styles.modalTitle}>Novo Usuário</Text>
            <TextInput style={styles.input} placeholder="Nome" value={nome} onChangeText={setNome} />
            <TextInput
              style={styles.input} placeholder="Email" value={email}
              onChangeText={setEmail} keyboardType="email-address" autoCapitalize="none"
            />
            <TextInput
              style={styles.input} placeholder="Senha" value={senha}
              onChangeText={setSenha} secureTextEntry
            />
            <TouchableOpacity style={styles.saveButton} onPress={handleCreate}>
              <Text style={styles.saveText}>Salvar</Text>
            </TouchableOpacity>
            <TouchableOpacity onPress={() => setModalVisible(false)}>
              <Text style={styles.cancelText}>Cancelar</Text>
            </TouchableOpacity>
          </View>
        </View>
      </Modal>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f5f5f5' },
  card: {
    backgroundColor: '#fff', marginHorizontal: 16, marginVertical: 6,
    padding: 16, borderRadius: 8, elevation: 1,
  },
  cardName: { fontSize: 16, fontWeight: '500', color: '#333' },
  cardEmail: { fontSize: 14, color: '#666', marginTop: 2 },
  cardStatus: { fontSize: 12, fontWeight: '500', marginTop: 4 },
  empty: { textAlign: 'center', color: '#999', marginTop: 40 },
  fab: {
    position: 'absolute', right: 24, bottom: 24,
    width: 56, height: 56, borderRadius: 28,
    backgroundColor: '#1a73e8', justifyContent: 'center', alignItems: 'center',
    elevation: 4,
  },
  fabText: { color: '#fff', fontSize: 28, lineHeight: 28 },
  modalOverlay: { flex: 1, backgroundColor: 'rgba(0,0,0,0.5)', justifyContent: 'center' },
  modalContent: { backgroundColor: '#fff', marginHorizontal: 24, borderRadius: 12, padding: 24 },
  modalTitle: { fontSize: 20, fontWeight: 'bold', marginBottom: 16 },
  input: {
    borderWidth: 1, borderColor: '#ddd', borderRadius: 8, padding: 12,
    marginBottom: 12, fontSize: 15,
  },
  saveButton: { backgroundColor: '#1a73e8', borderRadius: 8, padding: 14, alignItems: 'center' },
  saveText: { color: '#fff', fontWeight: '600', fontSize: 16 },
  cancelText: { color: '#e53935', textAlign: 'center', marginTop: 12, fontSize: 15 },
});
