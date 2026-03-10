"""
Final OpenSSL compatibility test - NO UNICODE
Author: Ivan
"""

import os
import subprocess
import tempfile
from cryptocore.crypto.aes import AESШифр
from cryptocore.crypto.modes import РежимECB


class OpenSSLFinalTest:
    def __init__(self):
        self.key_hex = "000102030405060708090a0b0c0d0e0f"
        self.key_bytes = bytes.fromhex(self.key_hex)
        self.results = []
        
        # Find OpenSSL
        try:
            result = subprocess.run(["openssl", "version"], 
                                   capture_output=True, 
                                   text=True)
            if result.returncode == 0:
                print("[OK] OpenSSL found")
                print("      Version: " + result.stdout.strip())
                self.openssl_available = True
            else:
                self.openssl_available = False
        except:
            self.openssl_available = False
    
    def encrypt_openssl(self, data):
        """Encrypt with OpenSSL"""
        if not self.openssl_available:
            return None
            
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(data)
            in_file = f.name
        
        out_file = in_file + ".enc"
        
        try:
            subprocess.run([
                "openssl", "enc", "-aes-128-ecb", "-e",
                "-K", self.key_hex,
                "-in", in_file,
                "-out", out_file
            ], check=True, capture_output=True)
            
            with open(out_file, 'rb') as f:
                result = f.read()
            return result
        except Exception as e:
            print("      OpenSSL error: " + str(e))
            return None
        finally:
            try:
                os.unlink(in_file)
                os.unlink(out_file)
            except:
                pass
    
    def encrypt_cryptocore(self, data):
        """Encrypt with CryptoCore"""
        cipher = РежимECB(self.key_bytes)
        return cipher.зашифровать(data)
    
    def run_test(self, name, data):
        """Run single test"""
        print("\n" + name)
        print("-" * 50)
        print("  Data length: " + str(len(data)) + " bytes")
        
        our = self.encrypt_cryptocore(data)
        print("  CryptoCore: " + our.hex()[:64] + "...")
        
        if self.openssl_available:
            ossl = self.encrypt_openssl(data)
            if ossl:
                print("  OpenSSL:    " + ossl.hex()[:64] + "...")
                
                if our == ossl:
                    print("  [OK] IDENTICAL")
                    self.results.append((name, "PASS"))
                else:
                    print("  [FAIL] DIFFERENT")
                    self.results.append((name, "FAIL"))
            else:
                print("  [WARN] OpenSSL error")
                self.results.append((name, "ERROR"))
        else:
            print("  [WARN] OpenSSL not available")
            self.results.append((name, "SKIP"))
    
    def run_all_tests(self):
        """Run all tests"""
        print("=" * 70)
        print("OPENSSL COMPATIBILITY TEST")
        print("=" * 70)
        print("Key: " + self.key_hex)
        print()
        
        # Test 1: Empty data
        self.run_test("TEST 1: Empty data", b"")
        
        # Test 2: 1 byte
        self.run_test("TEST 2: 1 byte", b"A")
        
        # Test 3: 15 bytes
        self.run_test("TEST 3: 15 bytes", b"X" * 15)
        
        # Test 4: 16 bytes
        self.run_test("TEST 4: 16 bytes", b"ABCDEFGHIJKLMNOP")
        
        # Test 5: 17 bytes
        self.run_test("TEST 5: 17 bytes", b"ABCDEFGHIJKLMNOPQ")
        
        # Test 6: 32 bytes
        self.run_test("TEST 6: 32 bytes", b"ABCDEFGHIJKLMNOP" * 2)
        
        # Test 7: Random 100 bytes
        self.run_test("TEST 7: Random 100 bytes", os.urandom(100))
        
        # Test 8: Text data
        text = b"This is a test message for OpenSSL"
        self.run_test("TEST 8: Text data", text)
        
        # Summary
        self.print_summary()
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 70)
        print("TEST SUMMARY")
        print("=" * 70)
        
        for name, status in self.results:
            print("{:<30} {}".format(name, status))
        
        print("\n" + "=" * 70)
        
        if self.openssl_available:
            passed = len([s for n,s in self.results if s == "PASS"])
            failed = len([s for n,s in self.results if s == "FAIL"])
            errors = len([s for n,s in self.results if s == "ERROR"])
            total = len([s for n,s in self.results if s != "SKIP"])
            
            print("Total tests: " + str(total))
            print("Passed:      " + str(passed))
            print("Failed:      " + str(failed))
            print("Errors:      " + str(errors))
            
            if passed == total:
                print("\nCONCLUSION: CryptoCore is IDENTICAL to OpenSSL")
                print("All tests passed successfully!")
            else:
                print("\nCONCLUSION: Differences found with OpenSSL")
        else:
            print("\nCONCLUSION: OpenSSL not available")
        
        print("=" * 70)


if __name__ == "__main__":
    test = OpenSSLFinalTest()
    test.run_all_tests()