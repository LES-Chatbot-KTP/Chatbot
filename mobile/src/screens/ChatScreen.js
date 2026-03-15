/**
 * Chat screen — send questions and receive RAG-based answers.
 */
import React, { useState, useEffect, useRef } from 'react';
import {
  View, Text, TextInput, TouchableOpacity, FlatList, StyleSheet,
  KeyboardAvoidingView, Platform, Alert, ActivityIndicator,
} from 'react-native';
import { getHistorico, askQuestion, createAvaliacao } from '../services/chatService';

export default function ChatScreen({ route }) {
  const { conversaId } = route.params;
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const flatListRef = useRef(null);

  useEffect(() => {
    loadHistorico();
  }, []);

  async function loadHistorico() {
    try {
      const data = await getHistorico(conversaId);
      const formatted = [];
      for (const item of data) {
        formatted.push({ id: `q-${item.id}`, type: 'question', text: item.texto_original });
        if (item.resposta) {
          formatted.push({
            id: `a-${item.resposta.id}`,
            type: 'answer',
            text: item.resposta.texto,
            fontes: item.resposta.fontes || [],
            respostaId: item.resposta.id,
          });
        }
      }
      setMessages(formatted);
    } catch {
      // Ignore if no history
    }
  }

  async function handleSend() {
    if (!input.trim()) return;

    const question = input.trim();
    setInput('');
    setMessages((prev) => [...prev, { id: `q-temp-${Date.now()}`, type: 'question', text: question }]);
    setLoading(true);

    try {
      const result = await askQuestion(conversaId, question);
      setMessages((prev) => [
        ...prev,
        {
          id: `a-${result.resposta.id}`,
          type: 'answer',
          text: result.resposta.texto,
          fontes: result.resposta.fontes || [],
          respostaId: result.resposta.id,
        },
      ]);
    } catch {
      Alert.alert('Erro', 'Não foi possível obter resposta');
    } finally {
      setLoading(false);
    }
  }

  async function handleRate(respostaId, nota) {
    try {
      await createAvaliacao(respostaId, nota);
      Alert.alert('Sucesso', 'Avaliação registrada!');
    } catch {
      Alert.alert('Erro', 'Não foi possível avaliar');
    }
  }

  function renderMessage({ item }) {
    const isQuestion = item.type === 'question';
    return (
      <View style={[styles.bubble, isQuestion ? styles.questionBubble : styles.answerBubble]}>
        <Text style={[styles.bubbleText, isQuestion && styles.questionText]}>{item.text}</Text>
        {!isQuestion && item.fontes && item.fontes.length > 0 && (
          <View style={styles.fontesContainer}>
            <Text style={styles.fontesTitle}>Fontes:</Text>
            {item.fontes.map((f, i) => (
              <Text key={i} style={styles.fonteText}>• {f.documento_titulo}</Text>
            ))}
          </View>
        )}
        {!isQuestion && item.respostaId && (
          <View style={styles.ratingContainer}>
            {[1, 2, 3, 4, 5].map((n) => (
              <TouchableOpacity key={n} onPress={() => handleRate(item.respostaId, n)}>
                <Text style={styles.star}>{'★'}</Text>
              </TouchableOpacity>
            ))}
          </View>
        )}
      </View>
    );
  }

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : undefined}
    >
      <FlatList
        ref={flatListRef}
        data={messages}
        keyExtractor={(item) => item.id}
        renderItem={renderMessage}
        contentContainerStyle={styles.list}
        onContentSizeChange={() => flatListRef.current?.scrollToEnd()}
      />

      <View style={styles.inputContainer}>
        <TextInput
          style={styles.textInput}
          placeholder="Digite sua pergunta..."
          value={input}
          onChangeText={setInput}
          editable={!loading}
        />
        <TouchableOpacity style={styles.sendButton} onPress={handleSend} disabled={loading}>
          {loading ? (
            <ActivityIndicator color="#fff" size="small" />
          ) : (
            <Text style={styles.sendText}>Enviar</Text>
          )}
        </TouchableOpacity>
      </View>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f5f5f5' },
  list: { padding: 16, paddingBottom: 8 },
  bubble: { padding: 12, borderRadius: 12, marginBottom: 8, maxWidth: '85%' },
  questionBubble: { backgroundColor: '#1a73e8', alignSelf: 'flex-end' },
  answerBubble: { backgroundColor: '#fff', alignSelf: 'flex-start', elevation: 1 },
  bubbleText: { fontSize: 15, color: '#333' },
  questionText: { color: '#fff' },
  fontesContainer: { marginTop: 8, borderTopWidth: 1, borderTopColor: '#eee', paddingTop: 6 },
  fontesTitle: { fontSize: 12, fontWeight: '600', color: '#666' },
  fonteText: { fontSize: 12, color: '#888', marginTop: 2 },
  ratingContainer: { flexDirection: 'row', marginTop: 6 },
  star: { fontSize: 20, color: '#ffc107', marginRight: 4 },
  inputContainer: {
    flexDirection: 'row', padding: 12, backgroundColor: '#fff',
    borderTopWidth: 1, borderTopColor: '#eee',
  },
  textInput: {
    flex: 1, backgroundColor: '#f5f5f5', borderRadius: 20,
    paddingHorizontal: 16, paddingVertical: 10, fontSize: 15,
  },
  sendButton: {
    backgroundColor: '#1a73e8', borderRadius: 20, paddingHorizontal: 20,
    justifyContent: 'center', marginLeft: 8,
  },
  sendText: { color: '#fff', fontWeight: '600' },
});
