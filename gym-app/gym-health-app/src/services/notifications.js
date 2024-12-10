
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
