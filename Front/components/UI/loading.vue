<template>
    <div v-if="NewVal===false" class="fixed bg-white w-full h-screen">
      <div class="flex w-full h-full">
        <div class="flex mx-auto my-auto h-52 w-52 animate-spin rounded-full border-[20px] border-solid border-current border-r-transparent align-[-0.125em] motion-reduce:animate-[spin_1.5s_linear_infinite]" role="status">
        </div>
      </div>
    </div>
</template>

<script>
    export default {
        props: {
            NewVal: Boolean
        }
    }
</script>