import helpers
from sentence_transformers import SentenceTransformer, util
NLP_MODEL = SentenceTransformer('all-MiniLM-L6-v2')


def link_provisions():
    field_names = ['ID', 'Agreement', 'Year', 'Part', 'Section', 'Provision Number', 'Provision Text']
    destination_path = 'C:/Users/marcs/Documents/provisionsProject/Data/master.csv'
    match_threshold = 0.9
    data = helpers.compile_row_ids()
    for i in range(len(data)):
        embedding1 = NLP_MODEL.encode(data[i][6], convert_to_tensor=True)
        print("embedding 1 complete")
        for j in range(len(data)):
            print("------------next provision---------------")
            if data[i][1] != data[j][1]:  # if it's not in the same agreement
                embedding2 = NLP_MODEL.encode(data[j][6], convert_to_tensor=True)
                print("embedding 2 complete")
                cosine_score = util.pytorch_cos_sim(embedding1, embedding2)
                print(f"cosine score {cosine_score}")
                if cosine_score >= match_threshold:
                    print(data[i][6] + "  ||  " + data[j][6])
                    # data[i].append(j)
                    # data[j].append(i)


link_provisions()


