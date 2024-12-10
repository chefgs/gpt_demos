
import React, { useEffect } from 'react';
import { View, Text } from 'react-native';
import { database, auth } from '../firebaseConfig';
import { scheduleReminder } from '../services/notifications';

const Home = () => {
    useEffect(() => {
        const userId = auth.currentUser.uid;
        database.ref(`users/${userId}/dietPlan`).once('value', snapshot => {
            const dietPlan = snapshot.val();
            if (dietPlan) {
                Object.entries(dietPlan.meals).forEach(([meal, { time, food }]) => {
                    scheduleReminder(time, `Time for ${meal}: ${food}`);
                });
            }
        });
    }, []);

    return (
        <View>
            <Text>Welcome to Your Diet Tracker</Text>
            <Text>Today's Reminders Set!</Text>
        </View>
    );
};

export default Home;
