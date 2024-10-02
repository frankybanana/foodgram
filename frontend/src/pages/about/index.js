import { Title, Container, Main } from '../../components'
import styles from './styles.module.css'
import MetaTags from 'react-meta-tags'
import image from '../../images/django.jpg';

const About = ({ updateOrders, orders }) => {

  return <Main>
    <MetaTags>
      <title>О проекте</title>
      <meta name="description" content="Фудграм - О проекте" />
      <meta property="og:title" content="О проекте" />
    </MetaTags>

    <Container>
      <h1 className={styles.title}>Привет!</h1>
      <div className={styles.content}>
        <div>
          <h2 className={styles.subtitle}>Что это за сайт?</h2>
          <div className={styles.text}>
            <p className={styles.textItem}>
              Это учебный проект, где я познакомилась с Джанго.
            </p>
            <div><img src={image} /></div>
          </div>
        </div>
      </div>

    </Container>
  </Main>
}

export default About
