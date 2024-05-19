const Footer = () => {
    return (
        <footer>
            <p>&copy; 2024 CloudEngine Labs. All rights reserved.</p>
            <style jsx>{`
                footer {
                    background: var(--background-header);
                    color: var(--text-header);
                    padding: 20px;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                }
            `}</style>
        </footer>
    );
};

export default Footer;
