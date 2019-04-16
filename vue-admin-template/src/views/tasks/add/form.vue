<template>
  <div class="add-user-from">
    <el-form ref="form"
             :model="form"
             label-width="100px">
      <!--prop表示验证的方式，与验证相关-->
      <el-form-item label="任务名称"
                    prop="name">
        <el-input v-model="form.name"
                  style="width: 60%" />
      </el-form-item>
      <el-form-item label="上传文件："
                    prop="playbook">
        <input ref="files"
               type="file"
               @change="getFile($event)">
        <!-- <input v-model="form.playbook" style="width: 60%">  这样是不行的-->
      </el-form-item>
      <el-form-item>
        <el-button type="primary"
                   @click="onSubmit($event)">创建</el-button>
        <el-button @click="onCancel">取消</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>
<script>
import { createautotask } from '@/api/tasks/tasks'
export default {
  name: 'TaskForm',
  props: {
    form: {
      type: Object,
      default () {
        return {
          name: '',
          playbook: ''
        }
      }
    }
  },
  data () {
    return {
      fileList: [],
      fileSizeIsSatisfy: true
    }
  },
  computed: {
    myHeader () {
      return {
        'Content-Type': 'text/plain'
      }
    },
    myData () {
      return {
        'businessId': this.form.fileId,
        'businessType': 'sys_file'
      }
    }
  },
  methods: {
    getFile (event) {
      // console.log(this.$refs.files.files[0])  通过event获取这行文件的所有信息
      // console.log(event)  所有上传信息在event.target里
      this.form.playbook = event.target.files[0] // 将文件塞到表单里
      console.log(this.form.playbook)
    },
    onSubmit (event) {
      this.$refs.form.validate((valid) => {
        if (!valid) {
          return
        }
        // 阻止元素发生默认的行为（例如，当点击提交按钮时阻止对表单的提交）
        event.preventDefault()
        const formData = new FormData() // 实例化一个新对象
        formData.append('name', this.form.name) // 将表单里的name,playbook塞进去
        formData.append('playbook', this.form.playbook)
        console.log(formData)

        const config = { // 定义请求头
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }
        createautotask(formData, config).then(res => { // 上传的时候带上我们自定义的请求头,后端就认识了,才能传成功
          this.$message({
            message: '创建成功',
            type: 'success'
          })
          this.$router.push({ path: '/tasks/list' }) // 请求成功跳转至列表页
        })
      })
    },
    onCancel () {
      this.$message({
        message: 'cancel!',
        type: 'warning'
      })
    },
    submitForm () {
    },
    cancel () {
    },
    uploadUrl () {
      return 'http://127.0.0.1:9000/api/task/playbook/19/01'
    },
    addFile (file, fileList) {
      this.fileList = fileList
      // 限制上传文件为5M
      var sizeIsSatisfy = file.size < 5 * 1024 * 1024
      if (sizeIsSatisfy) {
        return true
      } else {
        this.fileSizeIsSatisfy = false
        return false
      }
    },
    insert (formName) {
      console.log(formName)
      this.$refs.form.validate((valid) => {
        if (valid) {
          if (this.fileList.length <= 0) {
            this.$message.error('请至少上传一个文件！')
            return
          }
          if (!this.fileSizeIsSatisfy) {
            this.$message.error('上传失败！存在文件大小超过5M！')
            return
          }
          // 手动上传文件，在点击确认的时候 校验通过才会去请求上传文件的url
          this.$refs.upload.submit()
          createautotask(this.form).then((res) => {
            if (res.data.status === 200) {
              this.form = {}
              this.fileList = []
              this.dialogFormVisible = false
              this.$message.success('新增成功！')
              this.getUploadList(1)
            } else {
              this.$message.error(res.data.msg)
            }
          })
            .catch((error) => {
              this.$message.error(error)
            })
        } else {
          this.$message.error('error submit!!')
          return false
        }
      })
    }
  }
}
</script>

