<template>
  <div>
    <el-form ref="form"
             :model="form"
             label-width="80px">
      <el-form-item label="书名"
                    prop="name">
        <el-input v-model="form.name" />
      </el-form-item>
      <el-form-item label="作者"
                    prop="authors">
        <el-select v-model="form.authors"
                   multiple
                   filterable
                   style="width: 400px"
                   placeholder="请选择">
          <el-option v-for="item in author_list"
                     :key="item.id"
                     :label="item.name"
                     :value="item.id" />
        </el-select>
      </el-form-item>
      <el-form-item label="出版时间">
        <el-date-picker v-model="form.publication_date"
                        type="date"
                        value-format="yyyy-MM-dd"
                        placeholder="选择日期" />
      </el-form-item>
      <el-form-item label="出版社"
                    prop="publisher">
        <el-select v-model="form.publisher"
                   filterable
                   placeholder="请选择">
          <el-option v-for="item in publish_list"
                     :key="item.id"
                     :label="item.name"
                     :value="item.id" />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary"
                   @click="submitForm">立即创建</el-button>
        <el-button @click="cancel">取消</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { getAuthorList } from '@/api/books/author'
import { getPublishList } from '@/api/books/publish'
export default {
  name: 'BookForm',
  props: {
    form: {
      type: Object,
      default () {
        return {
          name: '',
          publication_date: '',
          authors: [],
          publisher: []
        }
      }
    }
  },
  data () {
    return {
      author_list: [],
      publish_list: [],
      state: 0,
      rules: {
        name: [
          { required: true, message: '请输入书名', trigger: 'blur' }
        ],
        publication_date: [
          { required: true, message: '请输入出版时间', trigger: 'blur' }
        ],
        publisher: [
          { required: true, message: '请输入出版设', trigger: 'blur' }
        ],
        authors: [
          { required: true, message: '请输入作者', trigger: 'blur' }
        ]
      }
    }
  },
  watch: {
    state () {
      this.fetchAuthors()
      this.fetchPublishs()
    }
  },
  created () {
    this.state = 1
  },
  methods: {
    cancel () {
      this.$emit('cancel')
    },
    submitForm () {
      this.$refs.form.validate(valid => {
        if (!valid) {
          return
        }
        this.$emit('submit', this.form)
      })
    },
    fetchAuthors () {
      getAuthorList().then(res => {
        console.log(res)
        this.author_list = res.results
      })
    },
    fetchPublishs () {
      getPublishList().then(res => {
        console.log(res)
        this.publish_list = res.results
      })
    }
  }
}
</script>
