FROM python:3.10.7
COPY . /app
WORKDIR /app
RUN pip install --upgrade revChatGPT
RUN pip install -r requirements.txt
RUN mkdir -p /root/.kaggle
RUN mkdir -p /app/generated
COPY kaggle.json /root/.kaggle/kaggle.json
RUN chmod 600 /root/.kaggle/kaggle.json
ENV MODE production
ENV PORT 8501
EXPOSE $PORT
CMD streamlit run Main_Page.py --server.port=$PORT --server.address=0.0.0.0