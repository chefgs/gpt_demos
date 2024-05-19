import Link from 'next/link';

const Header = () => {
    return (
        <header>
            <div className="logo">
                <img src="/images/logo.png" alt="CloudEngine Labs Logo" />
                <h1>CloudEngine Labs</h1>
                <p>Cloud Engineering Redefined</p>
            </div>
            <nav>
                <ul>
                    <li><Link href="/">Home</Link></li>
                    <li><Link href="/offerings">Offerings</Link></li>
                    <li><Link href="/contact">Contact Us</Link></li>
                    <li><Link href="/blogs">Blogs</Link></li>
                </ul>
            </nav>
            <style jsx>{`
                header {
                    background: #005b96;
                    color: #ffffff;
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
                    color: #ffffff;
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
                    color: #ffffff;
                    font-weight: 600;
                }
            `}</style>
        </header>
    );
};

export default Header;