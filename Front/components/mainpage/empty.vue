<template>
    <div class="flex flex-col bg-orange-500 w-5/6 mx-auto my-auto">
        <p class="flex text-3xl mt-10 mx-auto">Главная страница не выбрана.</p>
        <p class="flex text-3xl my-10 mx-auto">Перейдите в панель управления для настройки.</p>
        <NuxtLink class="flex mb-10 bg-green-500 w-1/6 h-[50px] hover:bg-green-700 text-white font-bold mx-auto my-auto py-2 px-2 rounded justify-center items-center" to="/controlpanel">Перейти</NuxtLink>
    </div>
</template>

<script>
    export default {
        
    }
</script>