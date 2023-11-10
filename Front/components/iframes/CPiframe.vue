<template>
    <div class="flex w-full">
      <iframe class="flex bg-green-500 w-full min-h-screen" :src="sendSRC" frameborder="0"/>
    </div>
</template>

<script>
    export default {
        props: {
            sendSRC: String
        }
    }
</script>