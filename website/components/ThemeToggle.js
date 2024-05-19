import { useState, useEffect } from 'react';

const ThemeToggle = () => {
    const [theme, setTheme] = useState('light');
    const [colorBlindMode, setColorBlindMode] = useState(false);

    useEffect(() => {
        const savedTheme = localStorage.getItem('theme');
        const savedColorBlindMode = localStorage.getItem('colorBlindMode');
        if (savedTheme) {
            setTheme(savedTheme);
            document.documentElement.setAttribute('data-theme', savedTheme);
        }
        if (savedColorBlindMode) {
            setColorBlindMode(JSON.parse(savedColorBlindMode));
            document.documentElement.setAttribute('data-color-blind-mode', JSON.parse(savedColorBlindMode));
        }
    }, []);

    const toggleTheme = () => {
        const newTheme = theme === 'light' ? 'dark' : 'light';
        setTheme(newTheme);
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
    };

    const toggleColorBlindMode = () => {
        const newColorBlindMode = !colorBlindMode;
        setColorBlindMode(newColorBlindMode);
        document.documentElement.setAttribute('data-color-blind-mode', newColorBlindMode);
        localStorage.setItem('colorBlindMode', newColorBlindMode);
    };

    return (
        <div className="theme-toggle">
            <i 
                className={`fas ${theme === 'light' ? 'fa-moon' : 'fa-sun'}`} 
                onClick={toggleTheme} 
                title={theme === 'light' ? 'Switch to Dark Mode' : 'Switch to Light Mode'}
            />
            <i 
                className={`fas ${colorBlindMode ? 'fa-eye-slash' : 'fa-eye'}`} 
                onClick={toggleColorBlindMode} 
                title={colorBlindMode ? 'Disable Color Blind Mode' : 'Enable Color Blind Mode'}
            />
            <style jsx>{`
                .theme-toggle {
                    display: flex;
                    gap: 10px;
                    align-items: center;
                    cursor: pointer;
                }
                .theme-toggle i {
                    font-size: 1.5rem;
                    cursor: pointer;
                    color: var(--text-header);
                }
            `}</style>
        </div>
    );
};

export default ThemeToggle;
