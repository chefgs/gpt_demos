import os

# Define folder structure and files
structure = {
    "gym-health-app": {
        "src": {
            "components": {},
            "screens": {
                "DietPlan.js": """
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
""",
                "Home.js": """
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
""",
            },
            "services": {
                "notifications.js": """
import messaging from '@react-native-firebase/messaging';

export const requestUserPermission = async () => {
    const authStatus = await messaging().requestPermission();
    const enabled = authStatus === messaging.AuthorizationStatus.AUTHORIZED ||
                    authStatus === messaging.AuthorizationStatus.PROVISIONAL;

    if (enabled) {
        console.log('Notification permissions enabled.');
    }
};

export const scheduleReminder = async (mealTime, message) => {
    const time = new Date(mealTime);
    const delay = time.getTime() - new Date().getTime();
    if (delay > 0) {
        setTimeout(() => {
            messaging().sendMessage({ body: message });
        }, delay);
    }
};
"""
            },
            "utils": {},
            "App.js": """
import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import Home from './screens/Home';
import DietPlan from './screens/DietPlan';

const Stack = createStackNavigator();

export default function App() {
    return (
        <NavigationContainer>
            <Stack.Navigator initialRouteName="Home">
                <Stack.Screen name="Home" component={Home} />
                <Stack.Screen name="DietPlan" component={DietPlan} />
            </Stack.Navigator>
        </NavigationContainer>
    );
}
""",
            "firebaseConfig.js": """
import firebase from 'firebase/app';
import 'firebase/auth';
import 'firebase/database';
import 'firebase/messaging';

const firebaseConfig = {
    apiKey: "YOUR_API_KEY",
    authDomain: "YOUR_APP_ID.firebaseapp.com",
    databaseURL: "https://YOUR_APP_ID.firebaseio.com",
    projectId: "YOUR_APP_ID",
    storageBucket: "YOUR_APP_ID.appspot.com",
    messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
    appId: "YOUR_APP_ID"
};

if (!firebase.apps.length) {
    firebase.initializeApp(firebaseConfig);
}

export const auth = firebase.auth();
export const database = firebase.database();
export const messaging = firebase.messaging();
"""
        },
        "android": {},
        "ios": {},
        ".env": "REACT_NATIVE_FIREBASE_API_KEY=YOUR_API_KEY\nREACT_NATIVE_FIREBASE_APP_ID=YOUR_APP_ID\n",
        "package.json": """
{
  "name": "gym-health-app",
  "version": "1.0.0",
  "main": "index.js",
  "scripts": {
    "start": "react-native start",
    "android": "react-native run-android",
    "ios": "react-native run-ios"
  },
  "dependencies": {
    "firebase": "^9.0.0",
    "react-native": "^0.64.2",
    "@react-native-firebase/app": "^12.0.0",
    "@react-native-firebase/messaging": "^12.0.0",
    "@react-navigation/native": "^6.0.0",
    "@react-navigation/stack": "^6.0.0"
  }
}
"""
    }
}

def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:
            with open(path, 'w') as file:
                file.write(content)

# Create the folder structure
base_path = os.getcwd()
create_structure(base_path, structure)
print("Project structure created successfully.")
