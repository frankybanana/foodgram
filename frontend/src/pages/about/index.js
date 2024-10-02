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
      <div className={styles.content}>
        <div>
          <h2 className={styles.subtitle}>Привет!</h2>
          <div className={styles.text}>
            <p className={styles.textItem}>
              Это учебный проект курса, где я познакомилась с Джанго.
            </p>
            <div><img src={image} /></div>
          </div>
        </div>
      </div>

    </Container>
  </Main>
}

export default About
