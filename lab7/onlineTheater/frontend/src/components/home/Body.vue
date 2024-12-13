<template>
    <div class="" style="z-index: 100;">
        <Sidebar></Sidebar>
        <div class="root_body">
            <a class="nav-link d-flex align-items-center" style="width: auto; margin: 0 auto">
                <h3 style="cursor: pointer; margin-left: 45px;">Рекомендации</h3>
                <i class="fa fa-chevron-right fa-1lg" style="margin-top: -1px; cursor: pointer; padding-left: 7px;"></i>
            </a>

            <!-- Индикатор загрузки -->
            <div v-if="isLoading" class="loading-indicator">
                <span>Загрузка...</span>
            </div>

            <div class="slider-container">
                <swiper :modules="modules" :slides-per-view="5" navigation class="slider">
                    <swiper-slide v-for="film in films" :key="film.id" style="">
                        <div class="film-container">
                            <div class="raiting-container" style="">
                                <span>{{ film.vote_average || 'N/A' }}</span>
                            </div>
                            <img 
                                class="film-img" 
                                src="https://avatars.mds.yandex.net/get-kinopoisk-image/10835644/9a7203bd-7f9d-4f45-bc39-cdf7d4156332/280x420" 
                                :alt="film.title" 
                                style="cursor: pointer;" 
                                @click="getRecommendations(film.title)"
                            />
                            <div class="" style="max-width: 150px;">
                                <p class="film-text" style="margin: 0 auto">{{ film.title }}</p>
                                <p style="font-size: 12px;">{{ film.release_date }}, {{ film.genres }}</p>
                            </div>
                        </div>
                    </swiper-slide>
                </swiper>
            </div>
        </div>
    </div>
</template>

<script>
import { ref, watch, onMounted } from 'vue';
import axios from 'axios';
import { Navigation } from 'swiper/modules';
import { Swiper, SwiperSlide } from 'swiper/vue';

import 'swiper/css';
import 'swiper/css/navigation';

import Sidebar from '@/components/home/Sidebar.vue';

export default {
    name: 'Home_Body',
    components: {
        Sidebar,
        Swiper,
        SwiperSlide,
    },
    props: {
        searchQuery: String, // Получаем поисковый запрос из родительского компонента
    },
    setup(props) {
        const films = ref([]);
        const recommendedFilms = ref([]);
        const isLoading = ref(false); // Добавляем состояние для загрузки
        const modules = [Navigation];

        // Функция получения рекомендаций
        const fetchRecommendations = async (title) => {
            isLoading.value = true;
            try {
                const response = await axios.get(`http://127.0.0.1:8000/api/v1/film/recommendation/${title}`);
                films.value = response.data; // Загружаем данные
            } catch (error) {
                console.error('Ошибка при получении рекомендаций:', error);
            } finally {
                isLoading.value = false;
            }
        };

        // Вызов рекомендаций при клике по картинке
        const getRecommendations = (filmTitle) => {
            fetchRecommendations(filmTitle);
        };

        // Загрузка рекомендаций, когда поисковый запрос изменяется
        watch(() => props.searchQuery, (newQuery) => {
            if (newQuery) {
                fetchRecommendations(newQuery); // Загружаем рекомендации по новому запросу
            }
        });

        // Начальная загрузка списка фильмов
        const loadFilms = async () => {
            isLoading.value = true;
            try {
                const response = await axios.get('http://127.0.0.1:8000/api/v1/film/recommendation/Ariel');
                films.value = response.data;
            } catch (error) {
                console.error('Ошибка при загрузке фильмов:', error);
            } finally {
                isLoading.value = false;
            }
        };

        onMounted(() => {
            loadFilms();
        });

        return {
            films,
            recommendedFilms,
            isLoading,
            modules,
            getRecommendations,
        };
    }
}
</script>

<style scoped>
.root_body {
    position: relative;
    padding-top: 75px;
    padding-left: 15rem;
}

.swiper-slide {
    width: 150px;
}

.film-container {
    transition: opacity 0.3s ease, transform 0.3s ease;
    width: 160px;
    margin-left: 2.8rem;
}

.film-img {
    max-width: 100%;
}

.film-text {
    transition: color 0.3s ease;
}

.film-container:hover .film-img {
    opacity: 0.6;
    transform: scale(1.01);
}

.film-container:hover .film-text {
    color: orange;
}

.film-container:hover .raiting-container {
    opacity: 0;
}

.raiting-container{
    margin-left: 10px;
    margin-top: 10px;
    font-size: 14px; 
    font-weight: bold;
    padding-right: 5px; 
    padding-left: 5px; 
    width: auto; 
    background-color: green; 
    position: absolute; 
    text-align: center;
}

/* Индикатор загрузки */
.loading-indicator {
    text-align: center;
    font-size: 18px;
    font-weight: bold;
    margin: 20px 0;
}
</style>
