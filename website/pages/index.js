import Layout from '../components/Layout';
import SEO from '../components/SEO';
import styles from '../styles/Home.module.css';

export default function Home() {
    return (
        <Layout>
            <SEO
                title="The Great Technology Company - Cloud Engineering Redefined"
                description="Amplify Your Cloud & DevOps Automation Journey with The Great Technology Company"
                keywords="Cloud, DevOps, Automation, Engineering"
                // image="/images/logo.png"
                url="https://yourdomain.com"
            />
            <div className="container">
                <div className="hero">
                    <h1>Amplify Your Cloud & DevOps Automation Journey</h1>
                    <button>Contact Us</button>
                </div>
                <p>The Great Technology Company Private Limited based out in the city of Chennai, India...</p>
            </div>
        </Layout>
    );
}
