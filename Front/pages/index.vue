<template>
  <div class="">
    <MainpageEmpty v-if="!main_page_data"/>
    <MainpageNotEmpty v-if="main_page_data" :getPageData="main_page_data"/>
  </div>
</template>

<script>
import axios from 'axios';
  export default {
    data() {
      return {
        main_page_data: null,
      }
    },
    created() {
      axios.get("http://localhost:1337/get_main_page")
      .then(response => {
        console.log(response.data.pagename);
        axios.post("http://localhost:1337/get_page_by_name/", {"pagename": response.data.pagename})
        .then (response => {
          this.main_page_data = response.data.Page;
          console.log(response.data.Page);
        })
        .catch (error => console.log(response))
      })
      .catch(error => console.log(error))
    }
  }
</script>