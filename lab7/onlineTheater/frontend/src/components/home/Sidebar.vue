<template>
    <div class="position-fixed d-flex flex-column p-3 border-end shadow" style="margin-top: 2rem; height: 100%; z-index: 100;">
        <ul class="nav flex-column mt-4">
            <li class="nav-item mb-3">
                <a href="#" class="nav-link text-secondary d-flex align-items-center">
                    <i class="fa fa-home fa-lg me-2" aria-hidden="true"></i>
                    <span>Домой</span>
                </a>
            </li>
            <li class="nav-item mb-3">
                <a href="#" class="nav-link text-secondary d-flex align-items-center">
                    <i class="fa fa-film fa-lg me-2" aria-hidden="true"></i>
                    <span>Смотреть</span>
                </a>
            </li>
            <li class="nav-item mb-3">
                <a href="#" class="nav-link text-secondary d-flex align-items-center">
                    <i class="fa fa-heart fa-lg me-2" aria-hidden="true"></i>
                    <span>Избранное</span>
                </a>
            </li>
            <li class="nav-item">
                <a href="#" class="nav-link text-secondary d-flex align-items-center">
                    <i class="fa fa-line-chart fa-lg me-2" aria-hidden="true"></i>
                    <span>Популярное</span>
                </a>
            </li>
        </ul>
    </div>
</template>

<style scoped>
.nav-link {
    transition: color 0.3s ease;
}

.nav-link:hover {
    color: white !important;
}
</style>
