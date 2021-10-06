
import utime
import ustruct


SPL_I2C_ADDR = const(0x55)


def read_spl(i2c, clientMQTT):
    print("Reading SPL...")

    try:
        # i2c.writeto(SPL_I2C_ADDR, bytes([0x01, 0xFF]))      # SPL Get
        i2c.writeto(SPL_I2C_ADDR, bytes([0x02, 0xFF]))      # SPL Get and Reset
        utime.sleep_ms(20)
    except Exception as e:
        print("Failed to write to SPL I2C:", e)

    try:
        spl_bytes = bytearray(32)
        i2c.readfrom_into(SPL_I2C_ADDR, spl_bytes)

        values = []
        for i in range(8):
            value_f = ustruct.unpack('>f', bytes(spl_bytes[b + i*4] for b in range(4)))
            values.append(value_f[0])
            # print("{:0.3f}".format(value_f[0]))
    except Exception as e:
        print("Failed to read from SPL I2C:", e)

    if clientMQTT:
        try:
            topic_name = 'WS-test/SPL/'
            clientMQTT.publish(topic=topic_name+"LAS",    msg=str(values[0]))
            clientMQTT.publish(topic=topic_name+"LASmax", msg=str(values[1]))
            clientMQTT.publish(topic=topic_name+"LASmin", msg=str(values[2]))
            clientMQTT.publish(topic=topic_name+"LAF",    msg=str(values[3]))
            clientMQTT.publish(topic=topic_name+"LAFmax", msg=str(values[4]))
            clientMQTT.publish(topic=topic_name+"LAFmin", msg=str(values[5]))
            clientMQTT.publish(topic=topic_name+"LAeq",   msg=str(values[6]))
            clientMQTT.publish(topic=topic_name+"STATUS", msg=str(values[7]))
            utime.sleep_ms(100) # Wait for MQTT to finish publishing
            print("SPL values sent to MQTT.")
        except Exception as e:
            print("Failed to send SPL values to MQTT!", e)



def read_spl_window(i2c, clientMQTT):
    print("Reading SPL Window...")

    try:
        i2c.writeto(SPL_I2C_ADDR, bytes([0x16, 0xFF]))
        utime.sleep_ms(20)
    except Exception as e:
        print("Failed to write to SPL I2C:", e)

    try:
        spl_bytes = bytearray(32)
        i2c.readfrom_into(SPL_I2C_ADDR, spl_bytes)

        window_values = []
        for i in range(8):
            value_f = ustruct.unpack('>f', bytes(spl_bytes[b + i*4] for b in range(4)))
            window_values.append(value_f[0])
            # print("{:0.3f}".format(value_f[0]))
    except Exception as e:
        print("Failed to read from SPL I2C:", e)

    if clientMQTT:
        try:
            topic_name = 'WS-test/SPL/'
            clientMQTT.publish(topic=topic_name+"Win-LAeq",  msg=str(window_values[0]))
            clientMQTT.publish(topic=topic_name+"Win-LAmax", msg=str(window_values[1]))
            clientMQTT.publish(topic=topic_name+"Win-LAmin", msg=str(window_values[2]))
            clientMQTT.publish(topic=topic_name+"Win-LA1",   msg=str(window_values[3]))
            clientMQTT.publish(topic=topic_name+"Win-LA10",  msg=str(window_values[4]))
            clientMQTT.publish(topic=topic_name+"Win-LA50",  msg=str(window_values[5]))
            clientMQTT.publish(topic=topic_name+"Win-LA90",  msg=str(window_values[6]))
            clientMQTT.publish(topic=topic_name+"Win-LA99",  msg=str(window_values[7]))
            utime.sleep_ms(100) # Wait for MQTT to finish publishing
            print("SPL window values sent to MQTT.")
        except Exception as e:
            print("Failed to send SPL window values to MQTT!", e)



def spl_readall(i2c):
    print("Reading SPL...")

    values = []
    window_values = []

    try:
        # i2c.writeto(SPL_I2C_ADDR, bytes([0x01, 0xFF]))      # SPL Get
        i2c.writeto(SPL_I2C_ADDR, bytes([0x02, 0xFF]))      # SPL Get and Reset
        utime.sleep_ms(20)
    except Exception as e:
        print("Failed to write to SPL I2C:", e)

    try:
        spl_bytes = bytearray(32)
        i2c.readfrom_into(SPL_I2C_ADDR, spl_bytes)

        for i in range(8):
            value_f = ustruct.unpack('>f', bytes(spl_bytes[b + i*4] for b in range(4)))
            values.append(value_f[0])
            # print("{:0.3f}".format(value_f[0]))
    except Exception as e:
        print("Failed to read from SPL I2C:", e)

    print("Reading SPL Window...")

    try:
        i2c.writeto(SPL_I2C_ADDR, bytes([0x16, 0xFF]))
        utime.sleep_ms(20)
    except Exception as e:
        print("Failed to write to SPL I2C:", e)

    try:
        spl_bytes = bytearray(32)
        i2c.readfrom_into(SPL_I2C_ADDR, spl_bytes)

        for i in range(8):
            value_f = ustruct.unpack('>f', bytes(spl_bytes[b + i*4] for b in range(4)))
            window_values.append(value_f[0])
            # print("{:0.3f}".format(value_f[0]))
    except Exception as e:
        print("Failed to read from SPL I2C:", e)

    return values, window_values



def spl_sendall(clientMQTT, values, window_values):
    if clientMQTT:
        try:
            topic_name = 'WS-test/SPL/'
            clientMQTT.publish(topic=topic_name+"LAS",    msg=str(values[0]))
            clientMQTT.publish(topic=topic_name+"LASmax", msg=str(values[1]))
            clientMQTT.publish(topic=topic_name+"LASmin", msg=str(values[2]))
            clientMQTT.publish(topic=topic_name+"LAF",    msg=str(values[3]))
            clientMQTT.publish(topic=topic_name+"LAFmax", msg=str(values[4]))
            clientMQTT.publish(topic=topic_name+"LAFmin", msg=str(values[5]))
            clientMQTT.publish(topic=topic_name+"LAeq",   msg=str(values[6]))
            clientMQTT.publish(topic=topic_name+"STATUS", msg=str(values[7]))
            utime.sleep_ms(100) # Wait for MQTT to finish publishing
            print("SPL values sent to MQTT.")
            topic_name = 'WS-test/SPL/'
            clientMQTT.publish(topic=topic_name+"Win-LAeq",  msg=str(window_values[0]))
            clientMQTT.publish(topic=topic_name+"Win-LAmax", msg=str(window_values[1]))
            clientMQTT.publish(topic=topic_name+"Win-LAmin", msg=str(window_values[2]))
            clientMQTT.publish(topic=topic_name+"Win-LA1",   msg=str(window_values[3]))
            clientMQTT.publish(topic=topic_name+"Win-LA10",  msg=str(window_values[4]))
            clientMQTT.publish(topic=topic_name+"Win-LA50",  msg=str(window_values[5]))
            clientMQTT.publish(topic=topic_name+"Win-LA90",  msg=str(window_values[6]))
            clientMQTT.publish(topic=topic_name+"Win-LA99",  msg=str(window_values[7]))
            utime.sleep_ms(100) # Wait for MQTT to finish publishing
            print("SPL window values sent to MQTT.")
        except Exception as e:
            print("Failed to send SPL values to MQTT!", e)



def spl_reset(i2c):
    print("SPL Reset...")

    try:
        i2c.writeto(SPL_I2C_ADDR, bytes([0x10]))
        utime.sleep_ms(20)
    except Exception as e:
        print("Failed to write to SPL I2C:", e)

    try:
        res = i2c.readfrom(SPL_I2C_ADDR, 1)
        if res != b'\x06':
            print("Error in SPL Reset:", res)
    except Exception as e:
        print("Failed to read from SPL I2C:", e)


def spl_set_window_size(i2c, size):
    if not (0x01 <= size <= 0x0F):
        print("Invalid window size:", size)
        return

    print("Setting window size:", size)

    try:
        i2c.writeto(SPL_I2C_ADDR, bytes([0x18, size]))
        utime.sleep_ms(20)
    except Exception as e:
        print("Failed to write to SPL I2C:", e)

    try:
        res = i2c.readfrom(SPL_I2C_ADDR, 1)
        if res != b'\x06':
            print("Error setting SPL window size:", res)
    except Exception as e:
        print("Failed to read from SPL I2C:", e)
