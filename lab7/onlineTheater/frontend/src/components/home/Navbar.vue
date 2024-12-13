<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top shadow">
      <div class="container-fluid">
        <ul class="navbar-nav mb-2 mb-lg-0" style="margin-left: 10rem;">
          <li class="nav-item">
            <a class="nav-link d-flex align-items-center gap-2 text-light" style="margin-right: 5rem;" href="#">
              <i class="fa fa-video-camera fa-lg"></i>
              Фильмы
            </a>
          </li>
          <li class="nav-item">
            <a class="nav-link d-flex align-items-center gap-2 text-light" href="#">
              <i class="fa fa-television fa-lg"></i>
              Мультфильмы
            </a>
          </li>
        </ul>
        <ul class="navbar-nav mb-2 mb-lg-0">
          <form class="d-flex" @submit.prevent="searchFilm">
            <div class="input-group" style="margin-right: 10rem;">
              <input 
                class="form-control" 
                type="search" 
                placeholder="Поиск..." 
                aria-label="Поиск" 
                v-model="searchQuery" 
              />
              <button class="btn btn-outline-light" type="submit">
                <i class="fa fa-search"></i>
              </button>
            </div>
          </form>
          <li class="nav-item" style="margin-right: 5rem;">
            <a class="nav-link text-light" href="#">Loreum</a>
          </li>
        </ul>
      </div>
    </nav>
  </div>
</template>

<script>
import { ref } from 'vue';

export default {
  name: 'Navbar',
  props: {
    // Принимаем функцию поиска через props
    onSearch: {
      type: Function,
      required: true,
    },
  },
  setup(props) {
    const searchQuery = ref(''); // Текст поиска

    // Функция, которая вызывает переданную функцию onSearch
    const searchFilm = () => {
      if (searchQuery.value.trim()) {
        props.onSearch(searchQuery.value); // Отправляем запрос на поиск
      }
    };

    return {
      searchQuery,
      searchFilm,
    };
  },
};
</script>

<style scoped>
.nav-link {
  color: white;
  transition: color 0.3s ease;
}

.nav-link:hover {
  color: #9ca3af !important;
}
</style>
