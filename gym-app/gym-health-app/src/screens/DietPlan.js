
import React, { useState } from 'react';
import { View, TextInput, Button, Text } from 'react-native';
import { database } from '../firebaseConfig';

const DietPlan = () => {
    const [breakfast, setBreakfast] = useState('');
    const [lunch, setLunch] = useState('');
    const [dinner, setDinner] = useState('');

    const saveDietPlan = () => {
        const userId = auth.currentUser.uid;
        database.ref(`users/${userId}/dietPlan`).set({
            breakfast,
            lunch,
            dinner,
        });
    };

    return (
        <View>
            <Text>Set Your Diet Plan</Text>
            <TextInput placeholder="Breakfast" value={breakfast} onChangeText={setBreakfast} />
            <TextInput placeholder="Lunch" value={lunch} onChangeText={setLunch} />
            <TextInput placeholder="Dinner" value={dinner} onChangeText={setDinner} />
            <Button title="Save Plan" onPress={saveDietPlan} />
        </View>
    );
};

export default DietPlan;
