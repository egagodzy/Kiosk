<template>
    <div class="flex flex-col min-h-screen">
      <IframesAllPagesModalwindow v-on:CloseModal="CloseModal" :testModal="TestModal"/>
      <IframesAllPagesButandinp v-on:OpenModal="OpenModal"/>
      <p class="flex mx-auto mt-5">Выберете главную страницу: </p>
      <select class="flex w-4/5 mx-auto mt-2 text-center" v-model="selected">
        <option value="">Не выбрана</option>
        <option v-for="page in pages">{{ page.pagename }}</option>
      </select>
      <div class="flex mx-auto mt-5 w-full">
        <span class="flex mx-auto my-2">Выбрано: {{ main_page_select }}</span>
        <button @click="SaveMainPage" class="bg-blue-500 hover:bg-blue-700 text-white mx-auto font-bold py-2 px-2 rounded">Выбрать</button>
      </div>
      <IframesAllPagesPagelist :pageList="pages"/>
    </div>
</template>

<script>
import axios from 'axios';
export default {
  data() {
    return {
      selected: '',
      main_page_select: '',
      TestModal: false,
      pages: null
    }
  },
  created() {
    axios.get("http://localhost:1337/get_all_pages")
    .then(response => {
      this.pages = response.data;
    })
    .catch(error => console.log(error));
    axios.get("http://localhost:1337/get_main_page")
    .then(response => {
      console.log(response.data);
      this.main_page_select = response.data.pagename
    })
    .catch(error => console.log(error));
  },
  methods: {
    OpenModal (SuperNew) {
            this.TestModal = SuperNew;
    },
    CloseModal (Close) {
            this.TestModal = Close;
    },
    SaveMainPage () {
      this.main_page_select = this.selected;
      axios.post("http://localhost:1337/change_main_page/", {"pagename": this.main_page_select})
      .then(response => {
        console.log(response.data);
      })
      .catch(error => console.log(error))
    }
  }
}
//@click="TestGoTo('/iframe/test')"
</script>