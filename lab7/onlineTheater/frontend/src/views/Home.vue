<template>
    <div class="font-serif">
        <Navbar @search="handleSearch" /> <!-- Слушаем событие поиска -->
        <Body :searchQuery="searchQuery" /> <!-- Передаем поисковый запрос в Body.vue -->
    </div>
</template>

<script setup>
import { ref } from 'vue';
import Body from '@/components/home/Body.vue';
import Navbar from '@/components/home/Navbar.vue';

const searchQuery = ref(''); // Состояние для поискового запроса

// Обработчик события поиска
const handleSearch = (query) => {
    searchQuery.value = query;
};
</script>
