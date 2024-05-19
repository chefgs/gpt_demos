import Layout from '../components/Layout';
import SEO from '../components/SEO';
import styles from '../styles/Home.module.css';

export default function Home() {
    return (
        <Layout>
            <SEO
                title="CloudEngine Labs - Cloud Engineering Redefined"
                description="Amplify Your Cloud & DevOps Automation Journey with CloudEngine Labs"
                keywords="Cloud, DevOps, Automation, Engineering"
                image="/images/logo.png"
                url="https://yourdomain.com"
            />
            <div className="container">
                <div className="hero">
                    <h1>Amplify Your Cloud & DevOps Automation Journey</h1>
                    <button>Contact Us</button>
                </div>
                <p>CloudEngine Labs Private Limited based out in the city of Chennai, India...</p>
                <img className={styles.myImageClass} src="/images/various-icons.png" alt="Icons representing various DevOps tools including GitHub, Terraform, and Kubernetes" />
            </div>
        </Layout>
    );
}
