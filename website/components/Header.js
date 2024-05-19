import Link from 'next/link';
import ThemeToggle from './ThemeToggle';

const Header = () => {
    return (
        <header>
            <div className="logo">
                <img src="/images/logo-only.png" alt="CloudEngine Labs Logo" />
                <div>
                    <h1>CloudEngine Labs</h1>
                    <p>Cloud Engineering Redefined</p>
                </div>
            </div>
            <nav>
                <ul>
                    <li><Link href="/">Home</Link></li>
                    <li><Link href="/offerings">Offerings</Link></li>
                    <li><Link href="/contact">Contact Us</Link></li>
                    <li><Link href="/blogs">Blogs</Link></li>
                </ul>
            </nav>
            <ThemeToggle />
            <style jsx>{`
                header {
                    background: var(--background-header);
                    color: var(--text-header);
                    padding: 20px;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                }

                .logo {
                    display: flex;
                    align-items: center;
                }

                .logo img {
                    width: 50px;
                    margin-right: 10px;
                }

                .logo h1 {
                    margin: 0;
                    font-weight: 600;
                    color: var(--text-header);
                }

                nav ul {
                    list-style-type: none;
                    margin: 0;
                    padding: 0;
                    display: flex;
                }

                nav ul li {
                    margin-right: 20px;
                }

                nav ul li a {
                    text-decoration: none;
                    color: var(--text-header);
                    font-weight: 600;
                }
            `}</style>
        </header>
    );
};

export default Header;
