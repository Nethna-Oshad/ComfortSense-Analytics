import { useState, useEffect } from 'react';
import { StyleSheet, Text, View, ActivityIndicator } from 'react-native';

export default function App() {
  const [data, setData] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  // IMPORTANT: Notice the IP address here matches the one Expo gave you!
  const API_URL = "http://172.20.10.2:8000/api/predict";

  const fetchPrediction = async () => {
    try {
      // We send simulated sensor data until the IoT team finishes the hardware
      const payload = {
        room_id: "Test Lab",
        session_start_time: new Date().toISOString(),
        readings: [{
          timestamp: new Date().toISOString(),
          temperature: 24.5,
          humidity: 55.0,
          noise: 40.0,
          CO2: 850.0,
          peopleCount: 25
        }]
      };

      const response = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      const result = await response.json();
      setData(result.predictions);
      setError(null);
    } catch (err) {
      setError("Cannot connect to server. Make sure Python FastAPI is running.");
    }
  };

  useEffect(() => {
    // Fetch data immediately, then update every 3 seconds
    fetchPrediction();
    const interval = setInterval(fetchPrediction, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>ComfortSense</Text>
      <Text style={styles.subtitle}>Live AI Predictions </Text>
      
      {!data && !error && <ActivityIndicator size="large" color="#007AFF" />}
      
      {error && <Text style={styles.errorText}>{error}</Text>}
      
      {data && (
        <View style={styles.card}>
          <Text style={styles.label}>Comfort Score</Text>
          <Text style={styles.value}>{data.Comfort_Score.toFixed(1)}%</Text>
          
          <View style={styles.divider} />
          
          <Text style={styles.label}>Attention Level</Text>
          <Text style={[styles.value, { color: data.Attention_Level === 'High' ? '#28a745' : '#dc3545' }]}>
            {data.Attention_Level}
          </Text>
          
          <Text style={styles.recommendation}>💡 {data.Actionable_Recommendation}</Text>
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: '#F2F2F7', padding: 20 },
  title: { fontSize: 32, fontWeight: '900', color: '#1C1C1E' },
  subtitle: { fontSize: 16, color: '#8E8E93', marginBottom: 30 },
  card: { backgroundColor: 'white', padding: 30, borderRadius: 20, width: '100%', elevation: 5, shadowColor: '#000', shadowOffset: { width: 0, height: 4 }, shadowOpacity: 0.1, shadowRadius: 10 },
  label: { fontSize: 14, color: '#8E8E93', textTransform: 'uppercase', fontWeight: '600', marginTop: 10 },
  value: { fontSize: 42, fontWeight: 'bold', color: '#007AFF', marginBottom: 10 },
  divider: { height: 1, backgroundColor: '#E5E5EA', marginVertical: 15 },
  recommendation: { fontSize: 16, fontWeight: '500', color: '#FF9500', marginTop: 20, textAlign: 'center' },
  errorText: { color: '#FF3B30', textAlign: 'center', margin: 20, fontSize: 16 }
});