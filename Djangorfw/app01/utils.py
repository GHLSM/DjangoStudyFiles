class myRespnse:
    def __init__(self):
        self.code = 1
        self.msg = 'success'

    # def get_dic(self):  # 在使用时取个见名知意的名字
    def responseData(self):
        return self.__dict__

