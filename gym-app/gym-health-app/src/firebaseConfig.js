
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
